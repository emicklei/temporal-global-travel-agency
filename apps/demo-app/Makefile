ROOT_DIR := $(abspath ../..)
IMAGE_NAME ?= demo-app:latest
DOCKERFILE := $(CURDIR)/Dockerfile

.PHONY: docker-build docker-run run test

# Build the demo-app Docker image from the repository root context.
docker-build:
	docker build -f $(DOCKERFILE) -t $(IMAGE_NAME) $(ROOT_DIR)

# Run the demo-app container and remove it when it exits.
docker-run:
	docker run --rm $(IMAGE_NAME)

# Run demo-app locally.
run:
	cd $(ROOT_DIR) && uv run --package demo-app python -m demo_app.main

# Run demo-app tests locally.
test:
	cd $(ROOT_DIR) && ./pants test apps/demo-app/tests::