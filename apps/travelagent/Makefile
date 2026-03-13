ROOT_DIR := $(abspath ../..)
IMAGE_NAME ?= travelagent:latest
DOCKERFILE := $(CURDIR)/Dockerfile

.PHONY: docker-build docker-run run start test

# Build the travelagent Docker image from the repository root context.
docker-build:
	docker build -f $(DOCKERFILE) -t $(IMAGE_NAME) $(ROOT_DIR)

# Run the travelagent container and remove it when it exits.
docker-run:
	docker run --rm $(IMAGE_NAME)

# Run the Temporal worker locally.
run:
	cd $(ROOT_DIR) && uv run --package travelagent python -m travelagent.main worker

# Start a hello workflow execution locally.
start:
	cd $(ROOT_DIR) && uv run --package travelagent python -m travelagent.main start --name "Temporal traveler"

# Run travelagent tests locally.
test:
	cd $(ROOT_DIR) && ./pants test apps/travelagent/tests::
