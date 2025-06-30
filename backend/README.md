# Backend

## Developer Sections

### Creating an alembic revision

```shell
docker compose -f docker-compose.dev.yml up postgres -d
docker compose -f docker-compose.dev.yml \
  run --rm --user $(id -u):$(id -g) --build backend \
  /app/.venv/bin/alembic revision --autogenerate -m "YOUR MESSAGE"
```

### Resetting Database

```shell
docker compose -f docker-compose.dev.yml down postgres -v
```
