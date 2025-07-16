# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.config import SETTINGS, AccountCreationMode
from app.core.dependencies import rate_limited
from app.services.mail import SUPPORTED as MAIL_SUPPORTED
from app.services.virus_scanning import SUPPORTED as VIRUS_SCANNING_SUPPORTED


router = APIRouter()


class AuthFeatures(BaseModel):
    local: bool
    oidc: bool
    magic_link: bool


class ServicesFeatures(BaseModel):
    mail: bool
    virus_scanning: bool


class FeaturesResponse(BaseModel):
    auth: AuthFeatures
    services: ServicesFeatures
    account_creation: AccountCreationMode


@router.get(
    path='/features',
    response_model=FeaturesResponse,
    dependencies=[Depends(rate_limited(capacity=20, refill_rate=20/60))],
)
async def get_features():
    r"""
    fetch which features are supported
    """
    return FeaturesResponse(
        auth=AuthFeatures(
            local=SETTINGS.AUTH_LOCAL is not None and SETTINGS.AUTH_LOCAL.ENABLED,
            oidc=SETTINGS.OIDC is not None,
            magic_link=SETTINGS.MAGIC_LINK is not None and SETTINGS.MAGIC_LINK.ENABLED,
        ),
        services=ServicesFeatures(
            mail=MAIL_SUPPORTED,
            virus_scanning=VIRUS_SCANNING_SUPPORTED,
        ),
        account_creation=SETTINGS.APP.ACCOUNT_CREATION,
    )
