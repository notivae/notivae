# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from pydantic import BaseModel, Field, ConfigDict, HttpUrl


__all__ = ['OpenIdToken', 'UserInfo', 'OpenIDConfiguration', 'OpenIDJwkKeys']


class OpenIdToken(BaseModel):
    token_type: str = Field(...)
    access_token: str = Field(...)
    expires_in: int = Field(...)
    refresh_token: t.Optional[str] = Field(None)
    scope: str = Field(...)
    id_token: str = Field(...)


class UserInfo(BaseModel):
    sub: str = Field(...)
    name: str = Field(..., alias="nickname")
    nickname: t.Optional[str] = Field(None)
    preferred_username: t.Optional[str] = Field(None)
    email: str = Field(...)
    email_verified: t.Optional[bool] = Field(False)
    picture: t.Optional[HttpUrl] = Field(None)
    locale: t.Optional[str] = Field(None)

    model_config = ConfigDict(populate_by_name=True)


class OpenIDConfiguration(BaseModel):
    issuer: HttpUrl = Field(...)
    authorization_endpoint: HttpUrl = Field(...)
    token_endpoint: HttpUrl = Field(...)
    userinfo_endpoint: t.Optional[HttpUrl] = Field(...)
    jwks_uri: HttpUrl = Field(...)


class OpenIDJwkKeys(BaseModel):
    keys: t.List[dict] = Field(...)
