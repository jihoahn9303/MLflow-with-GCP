#!/usr/bin/env bash

set -euo pipefail

mlflow server \
  --backend-store-uri "mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DATABASE_NAME}" \
  --default-artifact-root "${ARTIFACT_STORE}" \
  --host "${MLFLOW_HOST}" \
  --port "${MLFLOW_PORT}"