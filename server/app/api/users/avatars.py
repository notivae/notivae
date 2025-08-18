# -*- coding=utf-8 -*-
r"""

"""
import io
import os
import hashlib
import tempfile
import datetime as dt
from uuid import UUID
from pathlib import Path as FilePath
import structlog
from PIL import Image, UnidentifiedImageError
import blurhash as blurhashlib
from fastapi import APIRouter, HTTPException, status, Path as PathVar, Depends, File, UploadFile
from fastapi.responses import FileResponse
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, UserAvatar
from app.core.dependencies import get_async_session, get_current_user, rate_limited
from app.config import SETTINGS


router = APIRouter()
logger = structlog.getLogger()


@router.get(
    path="/{user_id}/avatar",
    response_class=FileResponse,
    dependencies=[
        Depends(rate_limited(capacity=100, refill_rate=10/1)),
        Depends(get_current_user),
    ],
)
async def get_users_avatar(
        session: AsyncSession = Depends(get_async_session),
        avatar_owner_id: UUID = PathVar(alias="user_id"),
):
    stmt = sql.select(UserAvatar).where(UserAvatar.owner_id == avatar_owner_id)
    avatar: UserAvatar = await session.scalar(stmt)
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has no avatar",
        )

    abs_path: FilePath = SETTINGS.ASSETS.STORAGE_ROOT / avatar.storage_path

    return FileResponse(
        path=abs_path,
        filename=abs_path.with_stem(f"{avatar_owner_id}").name,
    )


@router.put(
    path="/{user_id}/avatar",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limited(capacity=5, refill_rate=1/60))],
)
async def put_users_avatar(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user),
        avatar_owner_id: UUID = PathVar(alias="user_id"),
        file: UploadFile = File(),
):
    if user.id != avatar_owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't change another users avatar",
        )

    if file.content_type not in {"image/png", "image/jpeg", "image/webp"}:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported media type",
        )

    # load image
    try:
        img = Image.open(file.file)
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image",
        )
    except Image.DecompressionBombError:
        logger.warning(f"Some user tried to upload an image that was identified as a decompression-bomb", user=user.id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image too large",
        )

    # create avatar (cropped, resized)
    processed = process_avatar(img=img, size=512)

    # calculate blurhash
    blurhash = blurhashlib.encode(image=processed, x_components=4, y_components=4)

    # save to memory
    buffer = io.BytesIO()
    processed.save(fp=buffer, format="WEBP", quality=85, method=6, lossless=False)
    buffer.seek(0)

    # calculate sha
    sha256 = hashlib.sha256(buffer.getvalue()).hexdigest()

    # find and ensure storage location
    storage_path = FilePath("avatars", f"{avatar_owner_id}.webp")
    abs_path: FilePath = SETTINGS.ASSETS.STORAGE_ROOT / storage_path
    abs_path.parent.mkdir(parents=True, exist_ok=True)

    # atomic replace
    with tempfile.NamedTemporaryFile(suffix=".webp") as f:
        f.write(buffer.getvalue())
        f.flush()
        os.fsync(f.fileno())
        os.replace(f.name, abs_path)

    # update or create db entry
    stmt = sql.select(UserAvatar).where(UserAvatar.owner_id == avatar_owner_id)
    avatar = await session.scalar(stmt)
    if avatar:
        avatar.storage_path = str(storage_path)
        avatar.sha256_hash = sha256
        avatar.blurhash = blurhash
        avatar.created_at = dt.datetime.now(dt.UTC)
    else:
        avatar = UserAvatar(
            owner_id=avatar_owner_id,
            storage_path=str(storage_path),
            sha256_hash=sha256,
            blurhash=blurhash,
        )
        session.add(avatar)

    await session.commit()


@router.delete(
    path="/{user_id}/avatar",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limited(capacity=5, refill_rate=1/60))],
)
async def delete_users_avatar(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user),
        avatar_owner_id: UUID = PathVar(alias="user_id"),
):
    if user.id != avatar_owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't delete another users avatar",
        )

    stmt = sql.select(UserAvatar).where(UserAvatar.owner_id == avatar_owner_id)
    avatar: UserAvatar = await session.scalar(stmt)
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No avatar to delete",
        )

    abs_path: FilePath = SETTINGS.ASSETS.STORAGE_ROOT / avatar.storage_path
    abs_path.unlink(missing_ok=True)

    await session.delete(avatar)
    await session.commit()


def process_avatar(img: Image.Image, size: int = 512) -> Image.Image:
    """
    Crop to square, resize to fixed size, preserve alpha if present.
    Always outputs RGBA.
    """
    # Always convert to RGBA (handles all modes, keeps transparency if any)
    img = img.convert("RGBA")

    # Center crop
    width, height = img.size
    min_side = min(width, height)
    left = (width - min_side) // 2
    top = (height - min_side) // 2
    right = left + min_side
    bottom = top + min_side
    img = img.crop((left, top, right, bottom))

    # Resize to target size (always upscale/downscale)
    img = img.resize((size, size), Image.Resampling.LANCZOS)

    return img
