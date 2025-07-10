# Authentication via OpenID Connect (OIDC)

This guide explains how to set up authentication via any OpenID Connect compatible provider.

## Prerequisites

1. Access to a valid OpenID Connect provider (e.g. [Authentik](https://goauthentik.io/), [Auth0](https://auth0.com/), [Keycloak](https://www.keycloak.org/), [Okta](https://www.okta.com/))
2. Permissions to register a new application/client on the provider
3. Your application's domain or public URL for handling authentication callbacks

## Environment Variables

::: code-group
```dotenv [.env]
OIDC_CLIENT_ID=
OIDC_CLIENT_SECRET=
OIDC_DISCOVERY_URI=https://auth.example.com/.well-known/openid-configuration
OIDC_DISPLAY_NAME="OpenID"
```
:::

| Variable             | Description                                                                                          |
|----------------------|------------------------------------------------------------------------------------------------------|
| `OIDC_CLIENT_ID`     | The client/application ID from your OIDC provider                                                    |
| `OIDC_CLIENT_SECRET` | The client secret associated with the OIDC client ID                                                 |
| `OIDC_DISCOVERY_URI` | The URI pointing to the OIDC discovery document (usually ends in `.well-known/openid-configuration`) |
| `OIDC_DISPLAY_NAME`  | The name shown to users during login (e.g., "Login with OpenID")                                     |

:::: details Hidden Variables

::: code-group
```dotenv [.env]
OIDC_SCOPES="openid profile email"
```
:::

| Variable                | Description                                           |
|-------------------------|-------------------------------------------------------|
| `OIDC_SCOPES`           | Space-separated list of scopes requested during login |

::::

## Common Parameter

These values are often required by your OIDC provider.

| Parameter    | Value                                          |
|--------------|------------------------------------------------|
| Redirect URI | `https://<YOUR-DOMAIN>/api/auth/oidc/callback` |
