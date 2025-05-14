# Определяем переменные
VENV_DIR = venv
PYTHON = python3
PIP = $(VENV_DIR)/bin/pip
PYTEST = $(VENV_DIR)/bin/pytest
TEST_DIR := tests
SRC_DIR := app

.PHONY: install-req start test test-coverage remove-report


install-req:
	@echo "Install requirements ..."
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

test:
	@echo "Running tests ..."
	$(PYTEST) $(TEST_DIR) -v

start:
	@echo "Running tests ..."
	$(PYTHON) run.py

test-coverage:
	@echo "Running tests with coverage..."
	$(PYTEST) $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=term

test-coverage-report:
	@echo "Running tests with coverage report ..."
	$(PYTEST) $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=term --cov-report=html
	cd htmlcov
	google-chrome htmlcov/index.html

remove-report:
	@echo "Removing coverage report ..."
	rm -rf htmlcov
