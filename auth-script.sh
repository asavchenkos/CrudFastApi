#!/bin/bash

# Docker registry credentials
DOCKER_USERNAME="rahowa"
DOCKER_PASSWORD="Logitechc4"
DOCKER_REGISTRY="docker.io"

# Docker image details
IMAGE_NAME="rahowa/fast_api_nginx"
IMAGE_TAG=$1

# Authenticate with Docker
echo "$DOCKER_PASSWORD" | docker login --username $DOCKER_USERNAME --password-stdin $DOCKER_REGISTRY

# Build the Docker image
docker build -t $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG .

# Push the Docker image to the registry
docker push $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG

echo "Docker image pushed to $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG"