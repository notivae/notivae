# 🔐 Authentication

Notivae offers a flexible and self-contained authentication system, giving you full control over user data and login flows. It supports both traditional account-based login and external [OAuth/OIDC identity providers](#oauth-oidc-authentication), as well as passwordless login via [Magic-Link](./magic-link.md).

## Supported Authentication Methods

Users can authenticate using one or more of the following methods:

- [Password-based Authentication](./password.md) — traditional username/email + password login
- [OAuth/OIDC providers](#oauth-oidc-authentication) — login via third-party services (e.g., GitHub, Discord)
- [Magic-Link](./magic-link.md) — passwordless login via email

## Password-based login

If using password-based login, users can log in using either:

* Their **email address**
* Or a unique **username** (set during sign-up)

For email/password login details, refer to [Password-based Authentication](./password.md).

## OAuth / OIDC Authentication

Notivae supports logging in via third-party identity providers using the OIDC protocol. This enables users to authenticate without managing passwords directly.

Supported providers include:

- [Discord](./discord.md) <small>(Planned)</small>
- [GitHub](./github.md) <small>(Planned)</small>
- [GitLab](./gitlab.md) <small>(Planned)</small>
- [Google](./google.md) <small>(Planned)</small>
- [Reddit](./reddit.md) <small>(Planned)</small>
- [Spotify](./spotify.md) <small>(Planned)</small>
- [Twitch](./twitch.md) <small>(Planned)</small>
- Any identity provider compliant with [OpenID Connect](./oidc.md)

> [!TIP] Workaround
> While most providers aren't officially supported yet, many can still be used via generic OIDC configuration.  
> For example, Discord and GitLab are OIDC compatible and can be manually integrated:
> ```dotenv
> OIDC_CLIENT_ID=<your discord application's client ID>
> OIDC_CLIENT_SECRET=<your discord application's client secret>
> OIDC_DISCOVERY_URL=https://discord.com/.well-known/openid-configuration
> OIDC_SCOPES="identity email"
> OIDC_DISPLAY_NAME="Discord"
> ```

More providers will be documented with exact values and setup instructions once the integration layer stabilizes.

## Magic-Link Authentication

Magic-Link enables passwordless login through a secure link sent to the user's email address. This method is ideal for simplifying the login experience and reducing reliance on passwords.

- Can be used to **register new accounts**
- Can also be **linked to existing accounts** as an additional login method
- See the [Magic-Link Authentication Guide](./magic-link.md) for setup and behavior details

## System Management

A **system admin account** is created during the initial setup. This account has full access to all instance-level configuration and user management features.

## Session Management

Sessions are handled using secure HTTP-only cookies. No client-side tokens are stored in `localStorage` or exposed to JavaScript. All tokens are cryptographically signed and validated on the backend to ensure integrity and security.

## Planned Features

* Email verification and password reset flows
* Admin UI for user management (per instance)
* Optional 2FA support (TOTP-based)
* SSO login restrictions (e.g. only allow GitHub org members)

---

For more on how access is evaluated across documents and collections, see [Access Control](../../core-concepts/access-control.md).
