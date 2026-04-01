.PHONY: install lint fix check all test clean clean_cache
PRECOMMIT := uv run pre-commit

install:
	uv sync
	uv run pre-commit install

lint:
	$(PRECOMMIT) run --hook-stage manual --all-files

fix:
	$(PRECOMMIT) run --all-files

all:
	echo "`all` not implmemented yet"

test:
	uv run pytest

clean:
	rm -rf 	*.pyc, *.pyo, *.pyd \
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
