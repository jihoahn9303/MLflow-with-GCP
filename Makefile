include .envs/.gcp
include .envs/.tracking-server
export 

SHELL := /usr/bin/env bash
HOSTNAME := $(shell hostname)

ifeq (, $(shell which docker-compose))
	DOCKER_COMPOSE_COMMAND = docker compose
else
	DOCKER_COMPOSE_COMMAND = docker-compose
endif


# Returns true if the stem is a non-empty environment variable, or else raises an error.
guard-%:
	@#$(or ${$*}, $(error $* is not set))

# Deploy MLFlow using GCP Cloud Run
deploy: push
	./scripts/create-server.sh

# Run ssh tunnel for MLFlow
mlflow-tunnel:
	gcloud compute ssh "$${VM_NAME}" --zone "$${ZONE}" --tunnel-through-iap -- -N -L "$${MLFLOW_PORT}:localhost:$${MLFLOW_PORT}"

# Build docker containers with docker-compose
build:
	$(DOCKER_COMPOSE_COMMAND) build

# Push docker image to GCP Container Registery. Requires IMAGE_TAG to be specified.
push: guard-IMAGE_TAG build
	@gcloud auth configure-docker asia-northeast3-docker.pkg.dev --quiet
	@docker tag "${DOCKER_IMAGE_NAME}:latest" "$${GCP_DOCKER_REGISTRY_URL}:$${IMAGE_TAG}"
	@docker push "$${GCP_DOCKER_REGISTRY_URL}:$${IMAGE_TAG}"