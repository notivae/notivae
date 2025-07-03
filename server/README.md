# Notivae Server

The Notivae server is the backend entrypoint of the system, responsible for handling client communication, routing requests, managing authentication, and coordinating with other internal services such as the intelligence module. It exposes a clean API layer, acting as the glue between the frontend and the platform’s core logic.

## Developer Sections

### Creating an alembic revision

```shell
docker compose -f docker-compose.dev.yml up postgres -d
docker compose -f docker-compose.dev.yml \
  run --rm --user $(id -u):$(id -g) --build server \
  /app/.venv/bin/alembic revision --autogenerate -m "YOUR MESSAGE"
```

### Resetting Database

```shell
docker compose -f docker-compose.dev.yml down postgres -v
```
