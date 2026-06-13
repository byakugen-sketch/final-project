FROM jenkins/jenkins:lts-jdk17

USER root

# Install Docker CLI and curl
RUN apt-get update && apt-get install -y docker.io curl

# Install kubectl for ARM64 (Apple Silicon)
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl

# Install Helm
RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Allow jenkins user to use Docker
RUN usermod -aG docker jenkins

USER jenkins
