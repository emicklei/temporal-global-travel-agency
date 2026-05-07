ROOT_DIR := $(abspath ../..)
IMAGE_NAME ?= travelagent:latest
DOCKERFILE := $(CURDIR)/Dockerfile
# Docker Desktop on macOS may resolve host.docker.internal to IPv6 first,
# which can be unreachable from containers in some setups.
TEMPORAL_ADDRESS ?= 192.168.65.254:7233

.PHONY: docker-build docker-run run test

# Build the travelagent Docker image from the repository root context.
docker-build:
	docker build -f $(DOCKERFILE) -t $(IMAGE_NAME) $(ROOT_DIR)

# Run the travelagent container and remove it when it exits.
docker-run:
	docker run --rm -e TEMPORAL_ADDRESS=$(TEMPORAL_ADDRESS) $(IMAGE_NAME)

# Run the Temporal worker locally.
run:
	cd $(ROOT_DIR) && PYTHONPATH="$(ROOT_DIR)/apps/travelagent:$(ROOT_DIR)/pkgs:$(ROOT_DIR)/pkgs/logger/src" \
		uv run --package travelagent python -m worker.main

# Run travelagent tests locally.
test:
	cd $(ROOT_DIR) && ./pants test apps/travelagent/tests::

caller:
	cd $(ROOT_DIR) && PYTHONPATH="$(ROOT_DIR)/apps/travelagent:$(ROOT_DIR)/pkgs:$(ROOT_DIR)/pkgs/logger/src" \
		uv run --package travelagent python -m starter.caller

start:
	cd $(ROOT_DIR) && PYTHONPATH="$(ROOT_DIR)/apps/travelagent:$(ROOT_DIR)/pkgs:$(ROOT_DIR)/pkgs/logger/src" \
		uv run --package travelagent python -m starter.main
