.PHONY: help install dev test lint format clean docker-up docker-down migrate

help:
	@echo "V-Lab Fuel Gateway API - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install dependencies"
	@echo "  make dev           Install dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run           Run API server"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linters"
	@echo "  make format        Format code"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up     Start Docker containers"
	@echo "  make docker-down   Stop Docker containers"
	@echo "  make migrate       Run database migrations"
	@echo "  make load-data     Load initial data"
	@echo ""
	@echo "Database:"
	@echo "  make db-create-migration   Create new migration"
	@echo "  make db-upgrade            Apply migrations"
	@echo "  make db-downgrade          Revert migrations"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest -v

test-watch:
	pytest-watch

lint:
	ruff check app
	mypy app

format:
	black app
	isort app

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.mypy_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.ruff_cache' -exec rm -rf {} + 2>/dev/null || true

docker-up:
	docker-compose -f docker/docker-compose.yml up -d

docker-down:
	docker-compose -f docker/docker-compose.yml down

docker-logs:
	docker-compose -f docker/docker-compose.yml logs -f api

migrate:
	docker-compose -f docker/docker-compose.yml exec api alembic upgrade head

load-data:
	python scripts/load_data.py

db-create-migration:
	alembic revision --autogenerate -m "$(message)"

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1
