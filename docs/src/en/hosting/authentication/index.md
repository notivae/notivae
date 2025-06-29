# 🔐 Authentication

Notivae supports flexible, self-contained authentication options so you can stay in control of your user data and login flows. This includes support for traditional email/password accounts and external OAuth/OIDC providers.

## Email/Password Login

Email/password login is supported by default. When a user signs up:

- An account is created using the provided email and password
- A personal workspace is initialized
- The user is immediately authenticated

Email verification and password reset features are on the roadmap.

### Environment Requirements

You’ll need to configure the following environment variables:

````dotenv
AUTH_ENABLE_EMAIL=true
AUTH_EMAIL_FROM=notivae@example.com
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-smtp-user
SMTP_PASS=your-smtp-pass
`````

> 📧 Email delivery (e.g. for verification and password resets) will require working SMTP configuration. These features are not yet implemented, but the config is reserved.

## OAuth / OIDC Authentication

Notivae supports logging in via third-party identity providers using the OIDC protocol. This includes:

* [Google](./google.md)
* [GitHub](./github.md)
* [GitLab](./gitlab.md)
* [Discord](./discord.md)
* Any provider that supports [OpenID Connect](./oidc.md)

This allows users to log in without managing passwords directly.

### Setup Example (GitLab)

```dotenv
GITLAB_CLIENT_ID=your-client-id
GITLAB_CLIENT_SECRET=your-client-secret
GITLAB_ISSUER=https://gitlab.example.com/.well-known/openid-configuration
```

More providers will be documented with exact values and setup instructions once the integration layer stabilizes.

## Username Support

Users can log in using either:

* Email address
* Or a unique **username** (set at sign-up)

Usernames are helpful for mentions, short profile URLs, and reducing friction in shared workspaces (future).

## Session Management

Sessions are handled using secure HTTP-only cookies. No client-side tokens are stored in localStorage or exposed to JavaScript. All tokens are signed and validated on the backend.

## Planned Features

* Email verification and password reset flows
* Admin UI for user management (per instance)
* Optional 2FA support (TOTP-based)
* Anonymous / invite-only registration modes
* SSO login restrictions (e.g. only allow GitHub org members)

---

For more on how access is evaluated across documents and collections, see [Access Control](../core-concepts/access-control.md).
