.PHONY: install lint fix check

install:
	uv sync
	uv run pre-commit install

lint:
	uv run python -m pre_commit run --all-files

fix:
	uv run python -m pre_commit run --hook-stage manual --all-files

all:
	echo "`all` not implmemented yet"

test:
	uv run pytest

clean:
	rm -rf \
	*.pyc \
	*.pyo \
	*.pyd \
	.cache \
	build \
	dist \
	*.egg-info

clean_cache:
	rm -rf \
	__pycache__ \
	.mypy_cache \
	.pytest_cache \
	.ruff_cache \
