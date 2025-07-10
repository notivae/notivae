# 📧 Mail Support (Optional)

The mail service is **optional**, but highly recommended if you want to enable features like:

- Email verification for user signups
- Notification systems (e.g., for comment threads)
- Error notifications sent to administrators
- Admin approval mails for account creation if `APP_ACCOUNT_CREATION=restricted`
- Password reset flows
- Other user or admin-triggered messages

If not configured, these features will silently degrade or fallback to no-ops.

## Prerequisites

1. Access to a working SMTP server (e.g., Gmail, Mailgun, SendGrid, your own).
2. A valid sender email address and credentials (if required).

## Environment Variables

::: code-group
```dotenv [.env]
MAIL_SERVER=
MAIL_PORT=
MAIL_USE_CREDENTIALS=true
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_USE_TLS=false
MAIL_START_TLS=
MAIL_VALIDATE_CERTS=true
MAIL_TEMPLATES_DIR=
```
:::

| Variable               | Description                                                                                      |
|------------------------|--------------------------------------------------------------------------------------------------|
| `MAIL_SERVER`          | SMTP server hostname or IP address (e.g., `smtp.gmail.com`)                                      |
| `MAIL_PORT`            | SMTP port. Defaults: `465` if `MAIL_USE_TLS=true`, `587` if `MAIL_START_TLS=true`, else `25`     |
| `MAIL_USE_CREDENTIALS` | Whether to authenticate using `MAIL_USERNAME` and `MAIL_PASSWORD`                                |
| `MAIL_USERNAME`        | Username for SMTP login                                                                          |
| `MAIL_PASSWORD`        | Password (or app password) for SMTP login                                                        |
| `MAIL_FROM`            | Email address or `"Name <email@example.com>"` to use in the `From` header                        |
| `MAIL_USE_TLS`         | If `true`, use TLS immediately on connect. Mutually exclusive with `MAIL_START_TLS`              |
| `MAIL_START_TLS`       | If `true`, upgrade to TLS via STARTTLS after connecting. Overrides server STARTTLS support check |
| `MAIL_VALIDATE_CERTS`  | Whether to validate server certificates                                                          |
| `MAIL_TEMPLATES_DIR`   | Optional directory path to custom jinja email templates                                          |

::: details TLS vs STARTTLS

SMTP supports two common encryption modes:
- TLS (SMTPS): Encrypts the connection from the beginning (use port 465)
- STARTTLS: Starts unencrypted, then upgrades to TLS via the STARTTLS command (use port 587)

Set only one of the following:
- MAIL_USE_TLS=true: use SMTPS over port 465 (implicit TLS)
- MAIL_START_TLS=true: use SMTP with STARTTLS over port 587 (explicit TLS)
- Set both to false: use unencrypted SMTP, typically on port 25 (for internal or development servers)

Do not enable both TLS and STARTTLS.

:::

## Example Configurations

### Gmail (App Passwords)

::: code-group
```dotenv [.env]
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USE_CREDENTIALS=true
MAIL_USERNAME=notivae@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM="Notivae <notivae@gmail.com>"
MAIL_USE_TLS=true
MAIL_VALIDATE_CERTS=true
```
:::

### Mailgun

::: code-group
```dotenv [.env]
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USE_CREDENTIALS=true
MAIL_USERNAME=notivae@sandbox123.mailgun.org
MAIL_PASSWORD=your_mailgun_password
MAIL_FROM="Notivae <notivae@sandbox123.mailgun.org>"
MAIL_START_TLS=true
MAIL_VALIDATE_CERTS=true
```
:::

### Localhost (No Auth, No TLS)

::: code-group
```dotenv [.env]
MAIL_SERVER=localhost
MAIL_PORT=25
MAIL_USE_CREDENTIALS=false
MAIL_FROM="Notivae <notivae@example.com>"
MAIL_USE_TLS=false
MAIL_START_TLS=false
MAIL_VALIDATE_CERTS=false
```
:::

## Optional: Email Templates

The mail system comes with built-in HTML templates rendered using **Jinja2**.  
To override any of them, you can mount a custom template directory and set:

::: code-group
```dotenv [.env]
MAIL_TEMPLATES_DIR=/templates/emails
```
:::

Each custom template file must match the filename (and extension) of the default it's replacing.
The expected extension is: **`.html.j2`**

Modify you `docker-compose.yml` to mount your templates and set the environment variable.

::: code-group
```yaml [docker-compose.yml]
services:
  server:
    image: ghcr.io/notivae/server
    ...
    environment:
      MAIL_TEMPLATES_DIR: /templates/emails
    volumes:
      - ./my-custom-templates:/templates/emails:ro
```
:::

This will override any built-in template that has a matching `.html.j2` file in `./my-custom-templates`.

::: warning ⚠️ Important Notes 

* Only override templates you fully understand
* Do **not** attempt to create custom mail templates unless you are comfortable with:

  * Jinja2 syntax and escaping
  * HTML for email clients (tables, inline styles, etc.)
  * Required template filenames (e.g., `verify_email.html.j2`, `reset_password.html.j2`)
  * The variables available inside each template (not documented)
* Missing or broken templates won't fall back to the default built-in ones

:::

## Additional Notes

* `MAIL_FROM` supports both plain email addresses and `"Name <email@example.com>"` formats.
* If you're using 2FA on your email account (e.g., Gmail), you'll need an [App Password](https://support.google.com/accounts/answer/185833).
* Some SMTP servers require you to enable "less secure apps" or explicitly enable SMTP access.
