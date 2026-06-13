# Phase 1 — Flask Application & Docker

A simple Python Flask application containerized with Docker and published to Docker Hub.

---

## Application

Built with Flask, the app exposes two endpoints:

| Endpoint | Method | Response |
|----------|--------|----------|
| `/` | GET | `Hello, Doron!` |
| `/health` | GET | `{"status": "healthy"}` |

The `/health` endpoint is used by Kubernetes liveness and readiness probes in Phase 2.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)

---

## Docker Hub

The image is published at:

**`docker.io/uzumaki420/devops-experts-project:latest`**

Pull and run directly without building locally:
```bash
docker run -p 5001:5000 uzumaki420/devops-experts-project:latest
```

---

## Build and Run Locally

### 1. Build the image
```bash
docker build -t devops-experts-project .
```

### 2. Run the container
```bash
docker run -p 5001:5000 devops-experts-project
```

### 3. Open in browser
Visit: [http://localhost:5001](http://localhost:5001)

---

## Run with Docker Compose

```bash
docker-compose up
```

To stop:
```bash
docker-compose down
```

Enable debug mode:
```bash
FLASK_DEBUG=true docker-compose up
```

---

## Run Locally (without Docker)

```bash
pip install -r requirements.txt
python app.py
```

---

## Known Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Malformed YAML | `docker-compose.yml` had no indentation | Properly nested all keys |
| PDF artifacts in test file | Stray text pasted from PDF into `test_app.py` | Removed artifacts and fixed indentation |
| Flask not installed | Missing venv / system Python blocks pip | Created venv and ran `pip install -r requirements.txt` |
| Docker not running | Docker Desktop wasn't started | Launched Docker Desktop and waited for it to be ready |
| Port 5000 in use | macOS AirPlay Receiver holds port 5000 | Remapped host port to `5001` in `docker-compose.yml` |
| Port mismatch in container | `app.py` bound Flask to `5001` but Dockerfile exposed `5000` | Changed `app.run` to `port=5000` in `app.py` |
| Stale Docker cache | Rebuild didn't pick up port fix | Used `docker build --no-cache` / `docker compose up --build` |

---

## Project Structure

```
Phase 1/
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Docker Compose configuration
└── .dockerignore        # Files excluded from the Docker build context
```
