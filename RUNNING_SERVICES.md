# Services to bring back up

## 1. Minikube
```bash
minikube start
minikube tunnel   # keep open in a separate tab (or run with &)
```

## 2. Jenkins (docker-compose)
```bash
cd /Users/dovik/Projects/jenkins
docker compose up -d
docker network connect minikube jenkins-jenkins-1   # reconnect to minikube network for k8s access
```
Jenkins UI: http://localhost:8080

## 3. Prometheus & Grafana (already in Kubernetes — come up with minikube)
Port-forward after minikube starts:
```bash
# Prometheus
export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/instance=prometheus" -o jsonpath="{.items[0].metadata.name}")
kubectl --namespace monitoring port-forward $POD_NAME 9090 &

# Grafana
export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
kubectl --namespace monitoring port-forward $POD_NAME 3000 &
```
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (user: admin)

## 4. Redis (already in Kubernetes — comes up with minikube)
No action needed, deployed via Helm in the `databases` namespace.
