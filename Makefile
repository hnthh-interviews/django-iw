manage = poetry run python src/manage.py

cp-envs:
	cp .env.example .env

deps:
	poetry install --no-root

dev: cp-envs deps
	docker-compose up --build --detach
	make mr

fmt:
	poetry run ruff format src
	poetry run ruff check src --fix --unsafe-fixes
	poetry run toml-sort pyproject.toml

check:
	$(manage) makemigrations --check --dry-run --no-input
	$(manage) check
	poetry run ruff format --check src
	poetry run ruff check src
	poetry run toml-sort pyproject.toml --check

mr: fmt check test

run:
	$(manage) collectstatic --no-input
	$(manage) migrate
	$(manage) runserver

test:
	poetry run pytest --create-db
