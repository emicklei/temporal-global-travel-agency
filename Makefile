.PHONY: gen generate-models generate_models test fmt check

# requires schema2py
gen:
	bash scripts/tests/generate_api_models.sh
	python scripts/generate_api_docs.py

# compatibility aliases used by CI/workflows
generate-models: gen

generate_models: gen

test:
	./pants test --use-coverage :: '!scripts::'

# formats all code in the repo
# python, toml, javascript, etc.
fmt:
	uv run pre-commit run ruff --all-files || true
	uv run pre-commit run ruff-format --all-files || true
	uv run pre-commit run trailing-whitespace --all-files || true
	uv run pre-commit run end-of-file-fixer --all-files || true
	uv run pre-commit run pretty-format-json --all-files || true
	uv run pre-commit run ruff --all-files
	uv run pre-commit run ruff-format --all-files
	uv run pre-commit run trailing-whitespace --all-files
	uv run pre-commit run end-of-file-fixer --all-files
	uv run pre-commit run pretty-format-json --all-files

# runs repo validation checks in the pre-commit pipeline
check:
	uv run pre-commit run validate-api-schemas --all-files
	uv run pre-commit run check-generated-api-models --all-files
	uv run pre-commit run validate-git-tags --all-files
