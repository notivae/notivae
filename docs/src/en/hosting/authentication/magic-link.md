# Authentication via Magic-Link @icon:mail

This guide explains how to enable **magic-link authentication** as one of the available login methods for your Notivae.

With magic-link enabled, users can register or authenticate using a secure link sent to their email address—no password required. It's a lightweight alternative to password-based login and does not rely on external providers.

> [!IMPORTANT]
> Magic-link authentication requires a properly working mail configuration.  
> See the [Email Configuration Guide](../configuration/mail-support.md) for detailed setup instructions.

## Environment Variables

::: code-group
```dotenv [.env]
MAGIC_LINK_ENABLED=True
````
:::

| Variable             | Description                                |
|----------------------|--------------------------------------------|
| `MAGIC_LINK_ENABLED` | Enables the magic-link authentication flow |

## Setup Instructions

### Step 1: Enable Magic-Link Authentication

Set the following environment variable in your `.env` file:

::: code-group
```dotenv [.env]
MAGIC_LINK_ENABLED=True
```
:::

### Step 2: Configure Email Settings

Magic-link authentication depends on sending emails to users. You **must** have a working email system configured for this feature to work correctly. Follow the setup instructions in the [Email Configuration Guide](../configuration/mail-support.md).

If email isn't set up, magic-link authentication will prevent the startup.

### Step 3: Apply changes and restart Notivae

After setting the environment variable and ensuring email is configured, restart Notivae to apply the changes:

```shell
docker compose up -d --force-recreate
```

---

Once enabled:
- Users can register a new account using magic-link as their primary authentication method.
- Existing users can link magic-link authentication to their account for future logins.

This allows you to offer magic-link either as a standalone login option or as part of a multi-auth strategy alongside email+password or OAuth providers.

## Security Note

Magic-links are single-use and expire after they are consumed. This means each login attempt generates a new token that can only be used once. If a user tries to reuse an old link, it will be rejected for security reasons. This behavior helps prevent replay attacks and unauthorized access from previously issued links.
