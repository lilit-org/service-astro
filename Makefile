.PHONY: install install-dev server clean test lint server-dev server-dev-stop docker-logs server-prod server-prod-stop curl key

VENV := venv
VENV_BIN := $(VENV)/bin
PYTHON := python3.11
HOST := 0.0.0.0
PORT := 8000
APP := app.main:app

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt

install-dev: install
	$(VENV_BIN)/pip install -r requirements-dev.txt

server:
	$(VENV_BIN)/uvicorn $(APP) --reload --host $(HOST) --port $(PORT)

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test: install-dev
	$(VENV_BIN)/pytest

lint: install-dev
	$(VENV_BIN)/black .
	$(VENV_BIN)/isort .
	$(VENV_BIN)/flake8 .

server-dev:
	docker-compose up --build

server-dev-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f

server-prod:
	docker run -d -p 8080:8000 --name lilit-astro-prod lilit-astro:prod

server-prod-stop:
	docker stop lilit-astro-prod || true
	docker rm lilit-astro-prod || true

key:
	$(PYTHON) scripts/generate_api_key.py
