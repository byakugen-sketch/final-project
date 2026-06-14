# DevOps Experts Project

A Python Flask web application containerized with Docker, deployed on Kubernetes with Helm, and automated through a Jenkins CI/CD pipeline.

---

## Project Structure

```
final-project/
├── app.py                        # Flask application
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image definition
├── docker-compose.yml            # Local Docker Compose setup
├── Jenkinsfile                   # CI/CD pipeline definition
├── tests/
│   ├── conftest.py
│   └── test_app.py
├── k8s/                          # Raw Kubernetes manifests
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   ├── secret.yaml.example
│   ├── cronjob-healthcheck.yaml
│   └── cronjob-cleanup.yaml
├── helm/                         # Helm chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
└── jenkins/                      # Jenkins Docker setup
    ├── Dockerfile
    └── docker-compose.yml
```

---

## Application

The app exposes three endpoints:

| Endpoint | Method | Response |
|----------|--------|----------|
| `/` | GET | `{"message": "Hello, Doron!"}` |
| `/health` | GET | `{"status": "healthy"}` |
| `/version` | GET | `{"version": "1.0.0"}` |

Docker Hub image: `uzumaki420/devops-experts-project:latest`

---

## Part 1 — Docker

### Run with Docker Compose
```bash
docker-compose up
```

### Build and run manually
```bash
docker build -t devops-experts-project .
docker run -p 5001:5000 devops-experts-project
```

### Run tests
```bash
pytest tests/ -v
```

---

## Part 2 — Kubernetes with Minikube

### Prerequisites
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

### Start the cluster
```bash
minikube start --driver=docker
minikube addons enable metrics-server
```

### Create the secret
```bash
python3 -c "import secrets, base64; print(base64.b64encode(secrets.token_hex(32).encode()).decode())"
cp k8s/secret.yaml.example k8s/secret.yaml
# Edit k8s/secret.yaml and replace <base64-encoded-value>
```

> `secret.yaml` is gitignored — never commit it. Use the `.example` file as a template.

### Deploy
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/cronjob-healthcheck.yaml
kubectl apply -f k8s/cronjob-cleanup.yaml
```

### Access the app (Mac)
```bash
minikube tunnel
# App available at http://127.0.0.1:80
```

### Tear down
```bash
kubectl delete -f k8s/
minikube stop
```

---

## Part 3 — Helm & Jenkins CI/CD

### Prerequisites
- [Helm](https://helm.sh/docs/intro/install/)
- Docker Hub account and access token

### Deploy with Helm
```bash
helm upgrade --install flask-app ./helm --set secret.secretKey=<your-secret>
```

### Start Jenkins
```bash
cd jenkins
docker-compose up -d
docker exec jenkins-jenkins-1 cat /var/jenkins_home/secrets/initialAdminPassword
```

Jenkins runs at **http://localhost:8080**

### Jenkins configuration
1. Install suggested plugins
2. Add Docker Hub credentials — ID must be `dockerhub-credentials`
3. Create a Pipeline job:
   - SCM: Git → your repo URL
   - Branch: `*/main`
   - Script Path: `final-project/Jenkinsfile`

### Pipeline stages
| Stage | Action |
|-------|--------|
| Checkout | Pull latest code from GitHub |
| Build | Build Docker image |
| Test | Run pytest inside the container |
| Push | Push image to Docker Hub |
| Deploy | `helm upgrade --install` to Minikube |

---

## Known Issues & Fixes

| Issue | Fix |
|-------|-----|
| HPA shows `<unknown>` CPU | Enable metrics server: `minikube addons enable metrics-server` |
| Service stuck on `<pending>` external IP | Run `minikube tunnel` in a separate terminal |
| Jenkins can't find Jenkinsfile | Set Script Path to `final-project/Jenkinsfile` and disable lightweight checkout |
| Docker socket permission denied in Jenkins | Run Jenkins container as `user: root` |
| Helm deploy hits Jenkins instead of Kubernetes | Kubeconfig mounted to wrong path — use `/root/.kube/config` when running as root |
| Kubernetes unreachable after restart | Minikube changes API port on restart — update `host.docker.internal:<port>` in `jenkins/kubeconfig` |
