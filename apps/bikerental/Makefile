ROOT_DIR := $(abspath ../..)
IMAGE_NAME ?= bikerental:latest
DOCKERFILE := $(CURDIR)/Dockerfile

.PHONY: docker-build docker-run run test

# Build the bikerental Docker image from the repository root context.
docker-build:
	docker build -f $(DOCKERFILE) -t $(IMAGE_NAME) $(ROOT_DIR)

# Run the bikerental container and remove it when it exits.
docker-run:
	docker run --rm $(IMAGE_NAME)

# Run bikerental locally.
run:
	cd $(ROOT_DIR) && uv run --package bikerental python -m bikerental.main

# Run bikerental tests locally.
test:
	cd $(ROOT_DIR) && ./pants test apps/bikerental/tests::