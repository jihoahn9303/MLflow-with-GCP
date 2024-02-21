#!/usr/bin/env bash

MLFLOW_HOST=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/mlflow_host -H "Metadata-Flavor: Google")
MLFLOW_PORT=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/mlflow_port -H "Metadata-Flavor: Google")
ARTIFACT_STORE=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/artifact_store -H "Metadata-Flavor: Google")
MYSQL_USER=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/mysql_user -H "Metadata-Flavor: Google")
MYSQL_HOST=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/mysql_host -H "Metadata-Flavor: Google")
MYSQL_PORT=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/mysql_port -H "Metadata-Flavor: Google")
MYSQL_DATABASE_NAME=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/mysql_database_name -H "Metadata-Flavor: Google")
MYSQL_PASSWORD_SECRET_NAME=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/mysql_password_secret_name -H "Metadata-Flavor: Google")
GCP_DOCKER_REGISTRY_URL=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/gcp_docker_registry_url -H "Metadata-Flavor: Google")

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

echo '=========== Downloading Docker Image ============'
gcloud auth configure-docker --quiet asia-northeast3-docker.pkg.dev
echo "GCP_DOCKER_REGISTERY_URL = ${GCP_DOCKER_REGISTRY_URL}"
time sudo docker pull "${GCP_DOCKER_REGISTRY_URL}"

sudo docker run --init \
  --network host \
  --ipc host \
  --user root \
  --hostname "$(hostname)" --privileged \
  --log-driver=gcplogs \
  -e MYSQL_USER="${MYSQL_USER}" \
  -e MYSQL_PASSWORD=$(gcloud secrets versions access latest --secret="${MYSQL_PASSWORD_SECRET_NAME}") \
  -e MYSQL_HOST="${MYSQL_HOST}" \
  -e MYSQL_PORT="${MYSQL_PORT}" \
  -e MYSQL_DATABASE_NAME="${MYSQL_DATABASE_NAME}" \
  -e ARTIFACT_STORE="${ARTIFACT_STORE}" \
  -e MLFLOW_HOST="${MLFLOW_HOST}" \
  -e MLFLOW_PORT="${MLFLOW_PORT}" \
  ${GCP_DOCKER_REGISTRY_URL}