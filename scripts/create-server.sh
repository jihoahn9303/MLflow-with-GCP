#!/usr/bin/env bash

set -euo pipefail

# Create virtual machine(VM Instance)
gcloud compute instances create "${VM_NAME}" \
  --image "${IMAGE_NAME}" \
  --image-project "${IMAGE_PROJECT_ID}" \
  --boot-disk-auto-delete \
  --labels="${LABELS}" \
  --machine-type="${MACHINE_TYPE}" \
  --zone="${ZONE}" \
  --no-address \
  --network="${NETWORK}" \
  --subnet="${SUBNET}" \
  --scopes https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/cloud.useraccounts.readonly,https://www.googleapis.com/auth/cloudruntimeconfig \
  --project="${GCP_PROJECT_ID}" \
  --metadata-from-file=startup-script=./scripts/startup-script.sh \
  --metadata \
gcp_docker_registry_url="${GCP_DOCKER_REGISTRY_URL}:${IMAGE_TAG}",\
mlflow_host="${MLFLOW_HOST}",\
mlflow_port="${MLFLOW_PORT}",\
artifact_store="${ARTIFACT_STORE}",\
mysql_user="${MYSQL_USER}",\
mysql_host="${MYSQL_HOST}",\
mysql_port="${MYSQL_PORT}",\
mysql_database_name="${MYSQL_DATABASE_NAME}",\
mysql_password_secret_name="${MYSQL_PASSWORD_SECRET_NAME}"
