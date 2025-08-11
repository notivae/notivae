# @lucide:hammer Troubleshooting

This page helps you resolve common issues encountered while setting up or running Notivae using Docker.

If you're stuck on something not listed here, feel free to open an issue or check the [Contributing](../../other/contributing.md) guide.

## @lucide:puzzle Docker Setup Issues

### Docker/Docker Compose is not installed or not found

**Symptoms**
- Running `docker` or `docker compose` returns `command not found`.

**Solution**
- Ensure Docker and Docker Compose are installed correctly:
  - [Install Docker](https://docs.docker.com/get-docker/)
  - [Install Docker Compose](https://docs.docker.com/compose/install/)
- Restart your shell or terminal after installation.

## @lucide:container Container Won’t Start

### Ports are already in use

**Symptoms**
- Error like:
  ```
  Bind for 0.0.0.0:8766 failed: port is already allocated
  ```

**Solution**
- Another service is using the same port.
- Run:
  ```bash
  sudo lsof -i :8766
  ```
  and kill the conflicting process or modify the port in `docker-compose.yml`.

---

### Environment variables are not set or invalid

**Symptoms**
- Services crash on startup with unclear errors.
- Logs may reference missing configuration or fail to connect to other services.

**Solution**
- Ensure you have a `.env` file in the root directory (`/srv/notivae-stack`) and that it's configured correctly.
- Check for:
  - Missing values
  - Quotes around special characters
  - Line endings (use Unix line endings)

## @lucide:database Database Errors

### Database container exits immediately

**Symptoms**
- Running `docker compose up` shows the database container starting and then exiting or restarting in a loop.

**Possible Causes**
- Invalid environment variables
- Volume permission issues
- Existing corrupt volume

**Solutions**
- Double-check database config in `.env`
- Try resetting the volume (data will be lost):
  ```bash
  docker volume rm notivae_pgdata
  ```

## @lucide:app-window Frontend is Blank or Unresponsive

**Symptoms**
- You open `http://localhost:8766` and see a blank screen or a browser error.

**Solutions**
- Check if all containers are running:
  ```bash
  docker compose ps
  ```
- View frontend logs:
  ```bash
  docker compose logs web
  ```
- Make sure the backend is reachable from the frontend container (`localhost` inside a container ≠ your host machine)

## @lucide:brush-cleaning Cleanup Tips

### Removing all containers, volumes, and networks

If you want to start over clean:

```bash
docker-compose down -v
```

This will remove all associated volumes (e.g., database data). Be careful — this is irreversible.

## @lucide:bug Still Having Issues?

Open an issue on the repository with logs, your `.env` config (redact sensitive info), and a description of what’s not working.

We’re early in development and appreciate any feedback or bug reports!

