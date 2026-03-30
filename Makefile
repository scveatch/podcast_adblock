.PHONY: install lint fix check

install:
	uv sync
	uv run pre-commit install

fix:
	uv run pre-commit run --hook-stage manual

lint:
	uv run pre-commit
