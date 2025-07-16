# 🛡️ Security in Notivae

This section documents backend-level features and mechanisms designed to protect your Notivae instance from abuse, resource exhaustion, and unauthorized access. These measures apply to self-hosted deployments and may need adjustment depending on your environment.

> [!NOTE]
> These security features are built-in and require no external services. They apply automatically when Notivae is deployed.

## 🔐 Two-Factor Authentication (Planned)

Two-Factor Authentication (2FA) support is planned for future versions of Notivae. Once available, it will provide an additional layer of account security by requiring users to enter a time-based or device-generated code when logging in — especially useful for admin-level accounts or shared instances.


## 🔒 HTTPS & Reverse Proxy Configuration

Notivae is designed to run behind a reverse proxy like Nginx or Caddy, which should be configured to handle HTTPS and SSL termination.

Using HTTPS is essential to protect session tokens and sensitive data from being intercepted during transmission — especially important since authentication relies on httponly cookies.

> [!TIP]
> For guidance on setting up a secure reverse proxy, see the [Reverse Proxy Setup Guide](../start/installation/reverse-proxy.md).


## 🔃 Rate Limiting

To protect the server from misuse and ensure a stable experience for all users, Notivae applies automatic rate limits to certain API endpoints.

This means that if too many requests are made in a short time — whether by a user, a bot, or a misconfigured client — the server may temporarily reject further requests. In these cases, the response will clearly indicate that the limit was reached and suggest how long to wait before trying again.

Rate limits apply more strictly to unauthenticated users, while authenticated sessions are granted more flexibility.


## 🚫 Temporary Bans

If a client repeatedly hits the rate limit in a short time, Notivae may temporarily block further access from that user or IP address. This helps prevent abuse and reduces server load from bad actors or faulty automation.

Temporary bans are applied automatically and expire after a short period (e.g. one hour). Most users will never encounter this unless they are spamming requests or using unsupported tools.


## 🛡️ CSRF Protection
Notivae’s session authentication uses a `session_token` cookie with the following security flags:
- `HttpOnly`: Prevents JavaScript access
- `Secure`: Only sent over HTTPS
- `SameSite=Lax`: Allows form submissions but blocks most third-party cross-site requests

This setup provides basic protection against Cross-Site Request Forgery (CSRF) in most scenarios. While it's not a full CSRF defense mechanism, it's considered safe for APIs that do not accept cookie-authenticated cross-origin POSTs from third-party sites.

In future versions, Notivae may add stricter CSRF validation for endpoints that modify server-side state.
