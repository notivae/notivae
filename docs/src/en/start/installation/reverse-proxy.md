# @icon:shield Reverse Proxy Setup for Notivae

To make Notivae work correctly, you need to set up a **reverse proxy**. This is required even for local installations — not just for exposing it to the internet.

## @icon:circle-question-mark Why You Need a Reverse Proxy

By default, Notivae’s frontend and backend are served on **different ports**:

- Frontend: `http://localhost:8766`
- Backend: `http://localhost:8765`

But the frontend is hardcoded to call the backend via `/api` on the **same host and port**. Without a reverse proxy, this fails, and the web UI won’t work.

A reverse proxy solves this by:

- Making both frontend and backend accessible from **one unified domain**
- Forwarding frontend requests to the frontend container
- Forwarding `/api` requests to the backend container
- Optionally handling HTTPS for secure public access

## @icon:cog What You’ll Need

- A reverse proxy installed (see options below)
- A domain name (for internet-facing setups)
- Basic familiarity with editing config files or using Docker

## @icon:wrench Recommended Options

| Tool        | Why Use It                           | Docs                                        |
|-------------|--------------------------------------|---------------------------------------------|
| **Caddy**   | Easiest to set up, automatic HTTPS   | [caddyserver.com](https://caddyserver.com/) |
| **Traefik** | Designed for Docker, dynamic routing | [traefik.io](https://traefik.io/)           |
| **Nginx**   | Most flexible, widely supported      | [nginx.org](https://nginx.org/)             |

## @icon:file-code Example Configs

> [!IMPORTANT]
> These configuration examples assume your reverse proxy is running inside Docker (alongside Notivae, via `docker-compose`).  
> If you're using a system-wide reverse proxy (e.g., Traefik or Nginx on the host system), replace:
>
> - `backend:80` with `http://localhost:8765`
> - `frontend:80` with `http://localhost:8766`

### @icon:lock Caddy Example

If you're using Docker Compose, create a `Caddyfile` like this:

::: code-group
```caddyfile [Caddyfile]
notivae.localhost

handle_path /api/* {
    reverse_proxy backend:80
}

handle {
    reverse_proxy frontend:80
}
```
:::

And add a Caddy service to your `docker-compose.yml`:

::: code-group
```yaml [docker-compose.yml]
services:
  caddy:
    image: caddy:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
    depends_on:
      - frontend
      - backend
```
:::

> 💡 You’ll need to update `notivae.localhost` to your actual domain or host if not using `localhost`.

### @icon:cog Nginx Example

If you're using Docker Compose, create a `nginx.conf` like this:

::: code-group
```nginx [nginx.conf]
server {
    listen 80;
    server_name notivae.localhost;

    location /api/ {
        proxy_pass http://backend:80/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://frontend:80/;
    }
}
```
:::

And add an nginx service to your `docker-compose.yml`:

::: code-group
```yaml [docker-compose.yml]
services:
  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    ports:
      - "80:80"
    depends_on:
      - frontend
      - backend
```
:::

> [!INFO]
> You’ll need to update `notivae.localhost` to your actual domain or host if not using `localhost`.

## @icon:globe Exposing to the Internet

If you're self-hosting (e.g., on a home network or behind NAT), you'll need to expose your reverse proxy to the internet. There are two options:

### 1. Port Forwarding (Risky)
Open ports `80` and `443` on your router to your server. **Only recommended** if you know how to secure your server (firewalls, fail2ban, etc.).

### 2. Secure Tunnel (Recommended)

Use a tunnel service to make your reverse proxy public without opening any ports:

- **[Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)**
- **[Ngrok](https://ngrok.com/)**

These services let you tunnel traffic from a public domain to your local machine securely.

## @icon:brain Alternative: Tunnel-Only Setup (No Reverse Proxy)

If you’re using a tunnel provider like **Cloudflare Tunnel**, you can skip setting up a separate reverse proxy altogether.

Configure your tunnel to forward:

- `https://notivae.example.com/api/` → `http://localhost:8765`
- `https://notivae.example.com/` → `http://localhost:8766`

This works because most tunnel providers allow advanced path-based routing. Notivae only requires that `/api/*` hits the backend on the same domain.

> [!INFO] This is ideal for simple home or private setups with minimal config.

## @icon:check-square Final Checklist

- [x] You’ve confirmed `backend` and `frontend` are both running
- [x] You’ve either set up a reverse proxy *or* configured a tunnel-only setup
- [x] The `/api` path points to the backend, and `/` points to the frontend
- [x] If you're going public, you’ve configured HTTPS and/or tunneling

Once all of this is in place, open your browser at:

```
https://<your-domain-or-ip>
e.g. https://notivae.example.com
```

and the login-page should appear.

> [!TIP]
> Don't forget to run the setup wizard at
> ```
> https://<your-domain-or-ip>/#/init
> ```

---

> [!INFO]️ Having issues? Start by checking the container logs:
> 
> ```bash
> docker compose logs  # inspect all logs
> docker compose logs frontend  # inspect logs for a specific service
> ```

Still stuck? Look through our [troubleshooting guide](./troubleshooting.md) or otherwise open a [GitHub issue](https://github.com/notivae/notivae/issues).
