#!/usr/bin/env bash

set -euo pipefail

# ----------------------
# CONFIG
# ----------------------
REGION="us-east-1"
APP_NAME="ai-playground-app"
OLLAMA_NAME="ai-playground-ollama"
ECR_APP_OUTPUT="app_repository_url"
ECR_OLLAMA_OUTPUT="ollama_repository_url"

# Move into infra folder temporarily to run terraform
pushd infra > /dev/null

# ----------------------
# Update kubeconfig for kubectl access
# ----------------------
echo "🔧 Updating kubeconfig for kubectl access..."
aws eks update-kubeconfig --region us-east-1 --name $(terraform output -raw cluster_name)

# ----------------------
# Fetch ECR repo URLs from Terraform
# ----------------------
echo "🔍 Getting ECR repo URLs from Terraform..."
APP_REPO_URL=$(terraform output -raw ${ECR_APP_OUTPUT})
OLLAMA_REPO_URL=$(terraform output -raw ${ECR_OLLAMA_OUTPUT})

# Move back to current folder
popd > /dev/null

echo "📦 APP_REPO_URL: $APP_REPO_URL"
echo "📦 OLLAMA_REPO_URL: $OLLAMA_REPO_URL"

# ----------------------
# Authenticate with ECR
# ----------------------
echo "🔐 Logging into ECR..."
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "${APP_REPO_URL%%/*}"

# ----------------------
# Build and push app image
# ----------------------
echo "🐳 Building and pushing app image..."
docker buildx build --platform linux/amd64 -t ${APP_NAME}:latest -f Dockerfile.app .
docker tag ${APP_NAME}:latest ${APP_REPO_URL}:latest
docker push ${APP_REPO_URL}:latest

# ----------------------
# Build and push ollama image
# ----------------------
echo "🤖 Building and pushing ollama image..."
docker buildx build --platform linux/amd64 -t ${OLLAMA_NAME}:latest -f Dockerfile.ollama .
docker tag ${OLLAMA_NAME}:latest ${OLLAMA_REPO_URL}:latest
docker push ${OLLAMA_REPO_URL}:latest

# ----------------------
# Apply Kubernetes manifests
# ----------------------
echo "🚀 Deploying to Kubernetes..."

# Merge env vars into yaml and apply
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
envsubst < k8s/app-deployment.yaml | kubectl apply -f -
kubectl apply -f k8s/app-service.yaml
envsubst < k8s/ollama-deployment.yaml | kubectl apply -f -
kubectl apply -f k8s/ollama-service.yaml

echo "✅ Deployment complete!"
