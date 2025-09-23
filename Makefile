.PHONY: help init venv install lint format typecheck test test-cov tox docs

# Virtual environment (Windows and Unix, respectively)
VENV ?= .venv

ifeq ($(OS),Windows_NT)
	PY := $(VENV)/Scripts/python.exe
	PIP := $(VENV)/Scripts/pip.exe
else
	PY := $(VENV)/bin/python
	PIP := $(VENV)/bin/pip
endif

# Default target
.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@echo "  init			- Create venv and install project + dev deps"
	@echo "  install		- Install in editable mode (current interpreter)"
	@echo "  lint			- Run flake8 and isort --check-only"
	@echo "  format		 	- Run isort (and black if available)"
	@echo "  typecheck		- Run mypy/pyright (if available)"
	@echo "  test			- Run unit tests (pytest)"
	@echo "  test-cov		- Run tests with coverage report"
	@echo "  tox			- Run tox environments"
	@echo "  docs			- Build docs (MkDocs if available)"
	@echo "  dist			- Clean, test, build artifacts"
	@echo "  release		- Upload to PyPI with twine (if available)"
	@echo "  clean-*		- Remove caches and build artifacts"

# Environment and installation
venv:
	python -m venv $(VENV)

init: venv
	$(PIP) install --upgrade pip
	@if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt; fi
	$(PIP) install -e .
	@echo "Environment ready at $(VENV)"

install:
	$(PIP) install -e .

# Code quality
lint:
	flake8
	isort --check-only --diff .

format:
	isort .
	@command -v black >/dev/null 2>&1 && black . || echo "Black not installed; skipping."

typecheck:
	@command -v mypy >/dev/null 2>&1 && mypy src tests || echo "Mypy not installed; skipping."

# Tests
test:
	pytest -q

test-cov:
	PYTHONPATH=src pytest -q --cov=safe_input_veritas --cov-report=term-missing tests/

tox:
	tox

# Documentation (MkDocs optional)
docs:
	@command -v mkdocs >/dev/null 2>&1 && mkdocs build --clean || echo "MkDocs not installed; skipping."

docs-serve:
	@command -v mkdocs >/dev/null 2>&1 && mkdocs serve || echo "MkDocs not installed; skipping."

# Build and release
build:
	python -m build

dist: clean clean-build test build
	@echo "Artifacts ready in dist/"

release: dist
	@command -v twine >/dev/null 2>&1 && twine upload dist/* || echo "Twine not installed; skipping."

# Cleaning
clean: clean-build clean-pyc clean-cov
	@echo "Clean done."

clean-build:
	rm -rf build/ dist/ *.egg-info src/*.egg-info

clean-pyc:
	find . -name '__pycache__' -type d -exec rm -rf {} +
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete

clean-cov:
	rm -rf .coverage .coverage.* htmlcov/ .pytest_cache/ .mypy_cache/ .pytype/ .pyre/ .ruff_cache/ .nox/ .tox/
