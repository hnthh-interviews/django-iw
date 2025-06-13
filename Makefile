manage = poetry run python src/manage.py

cp-envs:
	cp .env.example .env

deps:
	poetry install --no-root

dev: cp-envs deps
	docker-compose up --build --detach
	make mr

fmt:
	poetry run ruff format src conftest.py
	poetry run ruff check src conftest.py --fix --unsafe-fixes
	poetry run toml-sort pyproject.toml

	make fmt-gitignore

fmt-gitignore:
	sort --output .gitignore .gitignore
	awk "NF" .gitignore > .gitignore.temp && mv .gitignore.temp .gitignore

check:
	$(manage) makemigrations --check --dry-run --no-input
	$(manage) check
	poetry run ruff format --check src conftest.py
	poetry run ruff check src conftest.py
	poetry run toml-sort pyproject.toml --check

mr: cp-envs fmt check test

run:
	$(manage) collectstatic --no-input
	$(manage) migrate
	$(manage) runserver

test:
	poetry run pytest --create-db
