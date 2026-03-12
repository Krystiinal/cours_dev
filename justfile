default:
    just --list

# Lancer l'application en mode dev
run-dev:
    uv run flask --app src run --debug

# Installer les dépendances de dev
install-dev:
    uv sync --locked --dev

# Supprimer le venv et les fichiers temporaires
clean:
    rm -rf .venv
    find . -type f -name '*.pyc' -delete
    find . -type d -name '__pycache__' -delete
