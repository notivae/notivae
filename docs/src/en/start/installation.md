
> [!IMPORTANT]
> Notivae is in early-stage development. No features are fully implemented yet.

# 🧰 Installation

Notivae is designed to be easy to self-host with Docker. The entire stack - frontend, backend and database - is orchestrated using `docker-compose`.

## 🔧 Prerequisites

Before you begin, make sure you have:

- **Docker** installed  
  [Install Docker](https://docs.docker.com/get-docker/)

- **Docker Compose** installed  
  [Install Docker Compose](https://docs.docker.com/compose/install/)

- Your system must meet the [minimum requirements](./requirements.md)

---

You will need a `docker-compose.yml` file to run Notivae. This file defines the services (frontend, backend, database), ports, and volumes.

You will also need a `.env` file. This file configures the behavior of the services.

Copy the following files to your local machine or server. We recommend placing them under `/srv/notivae-stack`.
The `docker-compose.yml` should work out-of-the box but could be adjusted to your needs.
The `.env` file **must** be customized to match your environment.

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
Once you have it in place:

```bash
docker compose up -d
```

This will:

* Start the backend API
* Start the Database
* Start the frontend
* Initialize persistent volumes and expose the ports of the backend and frontend

## ✅ Verify

After a few seconds, open your browser to:

```
http://localhost:8766
```

You should see the Notivae welcome screen or a prompt to sign up

## 🔁 Updating
To update Notivae to the latest version:

```shell
docker-compose pull
docker-compose up -d
```
This will fetch the latest version and restart the services.

## 🛑 Stopping the Stack

To stop the instance:
```shell
docker-compose down
```

## 🧪 Development Setup

If you're contributing, see the [Contributing](../other/contributing.md) guide for instructions on running each component in dev mode outside Docker.
