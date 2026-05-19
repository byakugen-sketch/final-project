# Hello 👋

A simple Python Flask application that returns a "Hello, World!" message.

---

## Requirements

- [Docker](https://www.docker.com/products/docker-desktop)

---

## Run Locally with Docker

### 1. Clone the repository
```bash
git clone https://github.com/byakugen-sketch/devops-experts-project-phase-1.git
cd devops-experts-project-phase-1
```

### 2. Build the Docker image
```bash
docker build -t hello .
```

### 3. Run the container
```bash
docker run -p 5000:5000 hello
```

### 4. Open in browser
Visit: [http://localhost:5000](http://localhost:5000)

---

## Run with Docker Compose

```bash
docker-compose up
```

To stop:
```bash
docker-compose down
```

---

## Push to Docker Hub

```bash
docker tag hello YOUR_DOCKERHUB_USERNAME/hello:latest
docker push YOUR_DOCKERHUB_USERNAME/hello:latest
```

---

## Project Structure

```
.
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image instructions
├── docker-compose.yml   # Docker Compose config
└── README.md            # Project documentation
```
