# Phase 2 — Kubernetes with Minikube

Deploys the Flask application from Phase 1 onto a local Kubernetes cluster using Minikube. Covers Deployments, Services, Horizontal Pod Autoscaling, ConfigMaps, Secrets, CronJobs, and health probes.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

---

## Setting Up the Kubernetes Cluster

### 1. Start Minikube
```bash
minikube start --driver=docker
```
This spins up a single-node Kubernetes cluster inside a Docker container on your machine.

### 2. Enable the Metrics Server
Required for Horizontal Pod Autoscaling to read CPU metrics:
```bash
minikube addons enable metrics-server
```

### 3. Verify the cluster is running
```bash
minikube status
kubectl get nodes
```
Expected output: one node named `minikube` with status `Ready`.

---

## Deploying the Application

Apply all manifests in the following order:

```bash
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml
kubectl apply -f cronjob-healthcheck.yaml
kubectl apply -f cronjob-cleanup.yaml
```

Verify everything is running:
```bash
kubectl get pods
kubectl get services
kubectl get hpa
kubectl get cronjobs
```

---

## Manifests Overview

### Deployment (`deployment.yaml`)
Manages the Flask application pods. Runs 2 replicas by default. Pulls the image `uzumaki420/devops-experts-project:latest` from Docker Hub.

Includes:
- **Liveness probe** — checks `/health` every 10s. Restarts the pod after 3 consecutive failures
- **Readiness probe** — checks `/health` every 5s. Removes the pod from the load balancer after 3 consecutive failures without restarting it
- **Resource requests/limits** — `100m` CPU request, `200m` CPU limit per pod (required for HPA)
- **Environment variables** — injected from ConfigMap and Secret (see below)

### Service (`service.yaml`)
Exposes the Flask app externally using a `LoadBalancer` type Service on port 80, forwarding traffic to port 5000 on the pods.

### Horizontal Pod Autoscaler (`hpa.yaml`)
Automatically scales the number of pods between 2 and 10 based on CPU usage. Triggers when average CPU across all pods exceeds 50% of their requested CPU.

### ConfigMap (`configmap.yaml`)
Stores non-sensitive configuration as key-value pairs injected into the pods as environment variables:
- `FLASK_DEBUG` — enables/disables Flask debug mode
- `APP_NAME` — application name

### Secret (`secret.yaml`)
Stores sensitive configuration base64-encoded. **Not committed to git** — use `secret.yaml.example` as a template:
```bash
cp secret.yaml.example secret.yaml
# Edit secret.yaml and replace placeholder with your base64-encoded value
# Generate a key: python3 -c "import secrets, base64; print(base64.b64encode(secrets.token_hex(32).encode()).decode())"
kubectl apply -f secret.yaml
```

Contains:
- `SECRET_KEY` — Flask secret key used for session signing

> **Note:** `secret.yaml` is intentionally excluded from version control via `.gitignore`. Committing secrets to a repository — even a private one — is a critical security risk. Once a secret is pushed to git, it lives in the commit history permanently and can be extracted even after deletion. This is standard practice from real-world production environments where exposed credentials have caused serious security incidents. In production, secrets are managed through dedicated tools such as HashiCorp Vault, AWS Secrets Manager, or Kubernetes Sealed Secrets — never stored in plain text in source control.

### CronJobs

**`cronjob-healthcheck.yaml`** — runs every minute, pings the Flask app and verifies it returns the expected response. Exits with code 1 if the check fails.

**`cronjob-cleanup.yaml`** — runs every hour, clears temporary files from `/tmp`.

---

## Accessing the App

The LoadBalancer requires a Minikube tunnel on Mac (Docker driver):
```bash
minikube tunnel
```
App is then available at **http://127.0.0.1:80**

Health endpoint: **http://127.0.0.1:80/health**

---

## Verifying Individual Components

**Check pod health and probes:**
```bash
kubectl describe pod <pod-name>
```

**Check HPA status and current CPU:**
```bash
kubectl get hpa
kubectl top pods
```

**View CronJob logs:**
```bash
kubectl get jobs
kubectl logs -l job-name=<job-name>
```

**Watch pods scale in real time:**
```bash
kubectl get pods -w
```

---

## Tear Down

```bash
kubectl delete -f cronjob-healthcheck.yaml
kubectl delete -f cronjob-cleanup.yaml
kubectl delete -f hpa.yaml
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
kubectl delete -f configmap.yaml
kubectl delete -f secret.yaml
minikube stop
```
