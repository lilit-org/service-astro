.PHONY: setup run clean test lint

VENV := venv
VENV_BIN := $(VENV)/bin
PYTHON := python3.11

setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt

run:
	$(VENV_BIN)/python main.py

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	$(VENV_BIN)/pytest

lint:
	$(VENV_BIN)/flake8 .
	$(VENV_BIN)/black --check .
	$(VENV_BIN)/isort --check-only .

format:
	$(VENV_BIN)/black .
	$(VENV_BIN)/isort .

