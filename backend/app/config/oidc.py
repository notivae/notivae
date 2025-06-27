# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, HttpUrl


__all__ = ["OidcSettings"]


class OidcSettings(BaseSettings):
    CLIENT_ID: str = Field(
        default=...,
        description="Client ID issued by the OpenID Connect provider",
    )
    CLIENT_SECRET: str = Field(
        default=...,
        description="Client secret associated with the OpenID Connect client",
    )

    AUTH_URI: HttpUrl = Field(
        default=...,
        description="Authorization endpoint URI for the OpenID Connect provider",
    )
    TOKEN_URI: HttpUrl = Field(
        default=...,
        description="Token endpoint URI for exchanging the authorization code for tokens",
    )
    USER_INFO_URI: HttpUrl = Field(
        default=...,
        description="User info endpoint URI to fetch authenticated user information",
    )
    LOGOUT_URI: HttpUrl = Field(
        default=...,
        description="Logout endpoint URI to redirect users after logout",
    )

    DISPLAY_NAME: str = Field(
        default="OpenID",
        description="Name to display for this identity provider in the frontend",
    )
    SCOPES: str = Field(
        default="openid profile email",
        description="Scopes requested from the OpenID Connect provider during authentication",
    )

    model_config = SettingsConfigDict(
        env_prefix="OIDC_",
        env_ignore_empty=True,
    )
