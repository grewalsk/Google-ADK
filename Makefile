.PHONY: help dev install lint format typecheck test docker-build docker-run docker-push deploy-dev deploy-prod

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: install ## Set up development environment
	poetry run pre-commit install
	@echo "Development environment set up successfully"

install: ## Install dependencies
	poetry install

lint: ## Run linting with ruff
	poetry run ruff check kalshi_trader/
	poetry run ruff check tests/

format: ## Format code with black
	poetry run black kalshi_trader/
	poetry run black tests/

typecheck: ## Run type checking with mypy
	poetry run mypy kalshi_trader/

test: ## Run tests with pytest
	poetry run pytest tests/ -v --cov=kalshi_trader

docker-build: ## Build Docker image
	docker build -t kalshi-trader:latest .

docker-run: ## Run Docker container locally
	docker run -p 8080:8080 --env-file .env kalshi-trader:latest

docker-push: ## Push Docker image to registry
	docker tag kalshi-trader:latest your-registry/kalshi-trader:latest
	docker push your-registry/kalshi-trader:latest

deploy-dev: ## Deploy to development environment
	@echo "Deploying to development..."
	# TODO: Add deployment commands for dev environment

deploy-prod: ## Deploy to production environment
	@echo "Deploying to production..."
	# TODO: Add deployment commands for prod environment

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 