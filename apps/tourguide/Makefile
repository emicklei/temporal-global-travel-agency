ROOT_DIR := $(abspath ../..)
IMAGE_NAME ?= tourguide:latest
DOCKERFILE := $(CURDIR)/Dockerfile

.PHONY: docker-build docker-run run test

# Build the tourguide Docker image from the repository root context.
docker-build:
	docker build -f $(DOCKERFILE) -t $(IMAGE_NAME) $(ROOT_DIR)

# Run the tourguide container and remove it when it exits.
docker-run:
	docker run --rm $(IMAGE_NAME)

# Run tourguide locally.
run:
	cd $(ROOT_DIR) && uv run --package tourguide python -m tourguide.main

# Run tourguide tests locally.
test:
	cd $(ROOT_DIR) && ./pants test apps/tourguide/tests::