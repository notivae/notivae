# -*- coding=utf-8 -*-
r"""

"""
import uuid
from urllib.parse import urlencode
from fastapi import APIRouter, Request, Query
from fastapi.responses import RedirectResponse
from app.config import SETTINGS
from app.core.security import oidc
from ._common import OidcState, encode_state


router = APIRouter()


@router.get("/redirect", response_class=RedirectResponse)
async def oidc_redirect(
        request: Request,
        next_url: str = Query(default="/", alias="next"),
):
    auth_uri = (await oidc.get_configuration(discovery_uri=SETTINGS.OIDC.DISCOVERY_URI)).authorization_endpoint

    redirect_uri = request.url_for("oidc_callback")
    nonce = str(uuid.uuid4())
    state = OidcState(
        nonce=nonce,
        next_url=next_url,
    )

    query_string = urlencode({
        'response_type': 'code',
        'client_id': SETTINGS.OIDC.CLIENT_ID,
        'redirect_uri': redirect_uri,
        'scope': SETTINGS.OIDC.SCOPES,
        'state': encode_state(state),
        'nonce': nonce,
    })
    url = f"{auth_uri}?{query_string}"
    return RedirectResponse(url=url)
