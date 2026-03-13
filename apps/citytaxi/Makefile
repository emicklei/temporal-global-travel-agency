ROOT_DIR := $(abspath ../..)
IMAGE_NAME ?= citytaxi:latest
DOCKERFILE := $(CURDIR)/Dockerfile

.PHONY: docker-build docker-run run test

# Build the citytaxi Docker image from the repository root context.
docker-build:
	docker build -f $(DOCKERFILE) -t $(IMAGE_NAME) $(ROOT_DIR)

# Run the citytaxi container and remove it when it exits.
docker-run:
	docker run --rm $(IMAGE_NAME)

# Run citytaxi locally.
run:
	cd $(ROOT_DIR) && uv run --package citytaxi python -m citytaxi.main

# Run citytaxi tests locally.
test:
	cd $(ROOT_DIR) && ./pants test apps/citytaxi/tests::