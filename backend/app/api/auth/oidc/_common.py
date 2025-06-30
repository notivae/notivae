# -*- coding=utf-8 -*-
r"""

"""
import base64
import pydantic


__all__ = [
    'OidcState',
    'encode_state',
    'decode_state',
]


class OidcState(pydantic.BaseModel):
    nonce: str
    next_url: str


def encode_state(state: OidcState) -> str:
    return base64.urlsafe_b64encode(state.model_dump_json().encode()).decode()


def decode_state(state: str) -> OidcState:
    return OidcState.model_validate_json(base64.urlsafe_b64decode(state).decode())
