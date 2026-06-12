#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

IMAGE=$(grep -E '^[[:space:]]*image:' yoink.yaml | head -1 | awk '{print $2}')
SERVICE=monty-django
PLATFORM=${PLATFORM:-linux/amd64}

TAG=$(git rev-parse --short HEAD)
if [ -n "$(git status --porcelain)" ]; then
  TAG="${TAG}-dirty-$(date +%H%M%S)"
fi

docker buildx build --platform "$PLATFORM" -t "${IMAGE}:${TAG}" --push .
yoink up --tag "${SERVICE}=${TAG}"
