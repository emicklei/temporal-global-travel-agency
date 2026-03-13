.PHONY: generate-models

generate-models:
	python scripts/generate_api_models.py

test:
	./pants test ::