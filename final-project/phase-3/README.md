# Phase 3 — Helm Chart & Jenkins CI/CD

Packages all Phase 2 Kubernetes manifests into a Helm chart and automates the full build, test, push, and deploy pipeline using Jenkins running inside Docker.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) running with `minikube tunnel` active
- [Helm](https://helm.sh/docs/intro/install/)
- Docker Hub account and access token
- GitHub repository with the project code

---

## Helm Chart

Installs the full application (Deployment, Service, HPA, ConfigMap, Secret, CronJobs) with a single command.

### Install
```bash
helm install flask-app ./phase-3 --set secret.secretKey=<your-secret>
```

### Upgrade (after changes)
```bash
helm upgrade flask-app ./phase-3 --set secret.secretKey=<your-secret>
```

### Uninstall
```bash
helm uninstall flask-app
```

The `secret.secretKey` is intentionally blank in `values.yaml` and must be passed via `--set` so it never appears in source control. Helm's `b64enc` filter handles the base64 encoding that Kubernetes requires.

---

## Jenkins Setup

Jenkins runs inside Docker and automates the pipeline on every push.

### Start Jenkins
```bash
cd phase-3/jenkins
docker-compose up -d
```

### Get the initial admin password
```bash
docker exec jenkins-jenkins-1 cat /var/jenkins_home/secrets/initialAdminPassword
```

Jenkins is available at **http://localhost:8080**

### Configure Jenkins

1. Unlock with the admin password and install suggested plugins
2. Add Docker Hub credentials:
   - Manage Jenkins → Credentials → (global) → Add Credentials
   - Kind: Username with password
   - ID: `dockerhub-credentials`
   - Password: Docker Hub access token (not account password)
3. Create a Pipeline job pointing to this repo with Script Path: `final-project/Jenkinsfile`

### Pipeline Stages

| Stage | What it does |
|-------|-------------|
| Checkout | Pulls latest code from GitHub |
| Build | Builds the Docker image from phase-1 |
| Test | Runs pytest inside the built container |
| Push | Pushes the image to Docker Hub |
| Deploy | Runs `helm upgrade --install` against the Minikube cluster |

---

## Known Issues & Fixes

| Issue | Fix |
|-------|-----|
| `helm install` failed with "release name already in use" | Used `helm upgrade --install` instead |
| Helm templates missing `apiVersion`/`kind` | `deployment.yaml` in repo was just a PDF excerpt — rewrote all 7 templates as complete manifests |
| Jenkins couldn't find Jenkinsfile | Repo root is one level above `final-project/` — set Script Path to `final-project/Jenkinsfile` and updated paths inside the Jenkinsfile |
| Docker socket permission denied in Jenkins | Mac Docker Desktop blocks `chmod` on the socket even with `privileged: true` — fixed by running the container as `user: root` |
| Helm deploy hit Jenkins login page instead of Kubernetes | Switched to `user: root` but kubeconfig was mounted to `/var/jenkins_home/.kube/config` — root's home is `/root`, so remounted to `/root/.kube/config` |
| Kubernetes cluster unreachable after restart | Minikube assigns a random API server port on each start — updated `host.docker.internal:<port>` in `jenkins/kubeconfig` to match |
| `tests/` not found inside container | `.dockerignore` excluded the tests folder — removed `tests/` from `.dockerignore` so pytest can run inside the container |

---

## Project Structure

```
phase-3/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── cronjob-healthcheck.yaml
│   └── cronjob-cleanup.yaml
└── jenkins/
    ├── Dockerfile
    ├── docker-compose.yml
    └── kubeconfig
```
