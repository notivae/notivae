# Authentication via Email + Password

This guide explains how to set up password-based authentication (commonly referred to as "local auth") for your application.

Password-based authentication works out of the box and is the simplest authentication mode to set up. It does not rely on any third-party authentication providers like Discord, GitHub, or Reddit—everything is handled internally by your application. This makes it an ideal choice for simple setups, single-user environments, or when you want full control over the authentication flow without external dependencies.

## Environment Variables

```dotenv
AUTO_LOCAL_ENABLED=True
```

| Variable              | Description                                  |
|-----------------------|----------------------------------------------|
| `AUTO_LOCAL_ENABLED`  | Enables the built-in local auth system       |

## Setup Instructions

### Step 1: Enable Local Authentication

Set the following environment variable in your deployment or `.env` file:
```dotenv
AUTO_LOCAL_ENABLED=True
```

### Step 2: Apply changes and restart Notivae

After updating your environment variables, restart Notivae to apply the changes:

```shell
docker compose up -d --force-recreate
```
