pipeline {
    agent any
    environment {
        GCP_PROJECT = 'your-gcp-project-id'
        REGION = 'us-central1'
        BACKEND_IMAGE = "us-central1-docker.pkg.dev/${GCP_PROJECT}/sirenprep-repo/backend:latest"
        FRONTEND_IMAGE = "us-central1-docker.pkg.dev/${GCP_PROJECT}/sirenprep-repo/frontend:latest"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/YOUR_GITHUB_USERNAME/SirenPrep_AI.git'
            }
        }
        stage('Build & Push Docker Images') {
            steps {
                script {
                    sh "gcloud auth configure-docker us-central1-docker.pkg.dev --quiet"
                    sh "docker build -t ${BACKEND_IMAGE} ./backend"
                    sh "docker push ${BACKEND_IMAGE}"
                    sh "docker build -t ${FRONTEND_IMAGE} ./frontend"
                    sh "docker push ${FRONTEND_IMAGE}"
                }
            }
        }
        stage('Deploy to Cloud Run') {
            steps {
                script {
                    // Deploy Backend
                    sh """
                    gcloud run deploy sirenprep-backend \
                        --image ${BACKEND_IMAGE} \
                        --platform managed \
                        --region ${REGION} \
                        --allow-unauthenticated \
                        --port 8080
                    """
                    // Deploy Frontend
                    sh """
                    gcloud run deploy sirenprep-frontend \
                        --image ${FRONTEND_IMAGE} \
                        --platform managed \
                        --region ${REGION} \
                        --allow-unauthenticated \
                        --port 80
                    """
                }
            }
        }
    }
}
