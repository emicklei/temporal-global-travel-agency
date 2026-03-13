ROOT_DIR := $(abspath ../..)
IMAGE_NAME ?= airliner:latest
DOCKERFILE := $(CURDIR)/Dockerfile

.PHONY: docker-build docker-run run test

# Build the airliner Docker image from the repository root context.
docker-build:
	docker build -f $(DOCKERFILE) -t $(IMAGE_NAME) $(ROOT_DIR)

# Run the airliner container and remove it when it exits.
docker-run:
	docker run --rm $(IMAGE_NAME)

# Run airliner locally.
run:
	cd $(ROOT_DIR) && uv run --package airliner python -m airliner.main

# Run airliner tests locally.
test:
	cd $(ROOT_DIR) && ./pants test apps/airliner/tests::