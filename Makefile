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

	make fmt-gitignore
	make fmt-conftest

fmt-gitignore:
	sort --output .gitignore .gitignore
	awk "NF" .gitignore > .gitignore.temp && mv .gitignore.temp .gitignore

fmt-conftest:
	poetry run ruff format conftest.py
	poetry run ruff check conftest.py --fix --unsafe-fixes

check:
	$(manage) makemigrations --check --dry-run --no-input
	$(manage) check
	poetry run ruff format --check src
	poetry run ruff check src
	poetry run flake8 src --select AZ400,AZ500
	poetry run toml-sort pyproject.toml --check

	make check-conftest

check-conftest:
	poetry run ruff format --check conftest.py
	poetry run ruff check conftest.py

mr: fmt check test

run:
	$(manage) collectstatic --no-input
	$(manage) migrate
	$(manage) runserver

test:
	poetry run pytest --create-db
