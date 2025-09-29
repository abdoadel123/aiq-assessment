.PHONY: help build up down migrate logs clean test

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

build: ## Build Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs
	docker-compose logs -f

migrate: ## Run database migrations
	docker-compose exec api python run_migrations.py

migrate-create: ## Create a new migration
	docker-compose exec api alembic revision --autogenerate -m "$(MSG)"

migrate-up: ## Apply migrations
	docker-compose exec api alembic upgrade head

migrate-down: ## Rollback one migration
	docker-compose exec api alembic downgrade -1

shell: ## Open Python shell in API container
	docker-compose exec api python

db-shell: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U user -d image_db

clean: ## Clean up containers and volumes
	docker-compose down -v
	rm -rf __pycache__ */__pycache__ */*/__pycache__

test: ## Run tests
	docker-compose exec api pytest

restart: down up ## Restart all services