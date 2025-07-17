
> [!IMPORTANT]
> Notivae is in early-stage development. No features are fully implemented yet.

# 🧰 Installation

Notivae can run on your own computer or server using **Docker**, a tool that bundles everything it needs. No need to install each part separately.

We’ll use a tool called `docker-compose` to launch all components – the app, its backend, and the database – all with one command.

## 🔧 Prerequisites

Make sure these are ready on your system:

- [X] **Docker**  
  [Install Docker](https://docs.docker.com/get-docker/)

- [X] **Docker Compose**  
  [Install Docker Compose](https://docs.docker.com/compose/install/)

- [X] A machine that meets the [minimum requirements](../requirements.md)

- [X] Basic knowledge of how to use a terminal (e.g., navigating folders, running commands)

---

## 📁 Setup Files

To run Notivae, you'll need two files:

1. **`docker-compose.yml`** – defines the services (frontend, backend, database), ports, and volumes.
2. **`.env`** – contains configuration settings like database passwords, ports, and secrets.

Copy the following files to your local machine or server. We recommend placing them under `/srv/notivae-stack`.
- The `docker-compose.yml` file works as-is but can be customized to your environment or use case.
- The `.env` file **must** be reviewed and adjusted. Each variable has a comment or description in the sample. For a deeper explanation, see [Configuration](../../hosting/configuration/index.md).

Your folder structure should look like this:

```text
📁 /srv/notivae-stack
 ┣ 📄 docker-compose.yml
 ┗ 📄 .env
```

> [!WARNING]
> These configuration files are currently in draft status and are not fully functional. Use them as a reference or base for manual setup until stable versions are released.

::: code-group

<<< @/assets/docker-compose.yml

<<< @/assets/.env.sample{dotenv}[.env]

:::

## ▶️ Start the Stack

From within the `/srv/notivae-stack` directory, run:

```bash
docker compose up -d
```

This command will:

- Start the **database** and **cache** (for storage)
- Start the **backend** (the engine)
- Start the **frontend** (the user interface)

Docker will automatically download any required images on the first run. This may take a while, depending on your internet connection.

## ✅ Verify

After a few seconds, run this command in your terminal:

```bash
curl http://localhost:8765/healtz
```

You should see a simple response like:

```json
{"status":"ok"}
```


If you see this message, it means the backend is running successfully and responding to requests.

However, you **won’t be able to access the web interface yet.** The frontend and backend are exposed on different ports and cannot communicate directly in this setup.

> [!INFO]
> 🛠️ To continue, you need to configure a [reverse proxy](./reverse-proxy.md) or another solution that connects the frontend to the backend under a unified address.  
> This is required before opening the web UI in your browser.

## 🌍 Connect Frontend and Backend

Notivae’s frontend expects to reach the backend at `/api` on the **same domain and port** — for example:

```text
https://notivae.example.com     → frontend
https://notivae.example.com/api → backend
```

However, in the current setup, the backend and frontend are exposed on **different ports**:

```text
http://localhost:8766 → Frontend
http://localhost:8765 → Backend 
```

This means they **can’t communicate properly** until you combine them under a unified domain or port.

The solution is a reverse proxy. A **reverse proxy** acts as a gateway that:

- Routes browser requests to the correct service (frontend or backend)
- Handles HTTPS (SSL) if needed
- Rewrites paths like `/api/*` to target the backend

This setup is required even if you're running Notivae locally.

Popular reverse proxy options:

- [Caddy](https://caddyserver.com/) — simple, automatic HTTPS
- [Traefik](https://traefik.io/traefik) — Docker-native, dynamic
- [Nginx](https://nginx.org/) — widely supported, configurable

> 📘 Need help setting it up?  
> See the [Reverse Proxy Guide](./reverse-proxy.md) for setup examples and config snippets.

> [!TIP]
> Hosting Notivae behind a home network? You may need a **tunnel** like [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/) or [Ngrok](https://ngrok.com/) to make it accessible from the internet.  
> This is also covered in the [Reverse Proxy Guide](./reverse-proxy.md).

## 🔁 Updating

To update Notivae to the latest version:

```shell
docker-compose pull
docker-compose up -d
```

This will:

- Pull the latest image versions
- Restart the containers using the updated versions

> [!WARNING]
> This command works only if you are omitting or using floating tags like `:latest` or `:dev` in your `docker-compose.yml`. If you pin versions explicitly in `docker-compose.yml`, you need to update the tags manually before running pull.

## 🛑 Stopping the Stack

To shut everything down:

```shell
docker-compose down
```

Your data (e.g., database files) will be preserved unless you remove the Docker volumes explicitly.
