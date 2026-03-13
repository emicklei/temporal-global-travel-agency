.PHONY: generate-models

gen:
	python scripts/generate_api_models.py

test:
	./pants test --use-coverage ::