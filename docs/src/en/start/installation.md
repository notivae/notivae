
> [!IMPORTANT]
> Notivae is in early-stage development. No features are fully implemented yet.

# 🧰 Installation

Notivae is designed to be easy to self-host with Docker. The entire stack - frontend, backend and database together using `docker-compose`.

## 🔧 Prerequisites

Before you begin, make sure you have:

- **Docker** installed  
  [Install Docker](https://docs.docker.com/get-docker/)

- **Docker Compose** installed  
  [Install Docker Compose](https://docs.docker.com/compose/install/)

- You support the minimum [System Requirements](./requirements.md)

---

You will need a `docker-compose.yml` file to run Notivae. This file defines the services (frontend, backend, database), ports, and volumes.

> 📄 A sample `docker-compose.yml` will be provided soon. You’ll be able to copy it into your project and adjust it as needed.

Once you have it in place:

```bash
docker-compose up -d
```

This will:

* Start the backend API
* Start the Database
* Start the frontend
* Initialize persistent volumes and expose on port `3000` by default

## ✅ Verify

After a few seconds, open your browser to:

```
http://localhost:3000
```

You should see the Notivae welcome page or signup screen.

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
