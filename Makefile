SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: run-dev
run-dev: ## Lancer l'application en mode dev
	uv run flask --app src run --debug

.PHONY: install-dev
install-dev: ## Installer les dépendances de dev
	uv sync --locked --dev

.PHONY: clean
clean: ## Supprimer le venv et les fichiers temporaires
	rm -rf .venv
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

.PHONY: help
help: ## Afficher l'aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
