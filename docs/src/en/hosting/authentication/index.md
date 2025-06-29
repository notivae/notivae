# 🔐 Authentication

Notivae offers a flexible and self-contained authentication system, giving you full control over user data and login flows. It supports both traditional account-based login and external [OAuth/OIDC identity providers](#oauth--oidc-authentication).

## Username Support

Users can log in using either:

* Email address
* Or a unique **username** (set during sign-up)

For email/password login details, refer to [Password-based Authentication](./password.md).

## OAuth / OIDC Authentication

Notivae supports logging in via third-party identity providers using the OIDC protocol. This enables users to authenticate without managing passwords directly.

Supported providers include:

- [Google](./google.md)
- [GitHub](./github.md)
- [GitLab](./gitlab.md)
- [Discord](./discord.md)
- Any identity provider compliant with [OpenID Connect](./oidc.md)

### Setup Example (GitLab)

```dotenv
GITLAB_CLIENT_ID=your-client-id
GITLAB_CLIENT_SECRET=your-client-secret
GITLAB_ISSUER=https://gitlab.example.com/.well-known/openid-configuration
```

More providers will be documented with exact values and setup instructions once the integration layer stabilizes.

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
