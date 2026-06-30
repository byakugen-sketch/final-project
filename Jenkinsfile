pipeline {
    agent any

    environment {
        IMAGE_NAME = "uzumaki420/devops-experts-project"
        IMAGE_TAG  = "latest"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Scan') {
            steps {
                sh '''
                    docker run --rm \
                      -v /var/run/docker.sock:/var/run/docker.sock \
                      aquasec/trivy image \
                      --exit-code 1 \
                      --severity CRITICAL,HIGH \
                      --ignore-unfixed \
                      uzumaki420/devops-experts-project:latest
                '''
            }
        }
        stage('Test') {
            steps {
                sh "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m pytest tests/ -v"
            }
        }

        stage('Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy') {
            steps {
                sh "helm upgrade --install flask-app ./helm --namespace flask-app --create-namespace --set secret.secretKey=${IMAGE_TAG}"
            }
        }
    }

    post {
        success { echo 'Pipeline completed successfully' }
        failure { echo 'Pipeline failed' }
    }
}
