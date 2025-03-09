.PHONY: install-requirements
install-requirements:
	venv/bin/pip install -r requirements.txt

.PHONY: static
static:
	python ./src/manage.py collectstatic

.PHONY: run-server
run-server:
	python ./src/manage.py runserver

.PHONY: assets
assets:
	npx tailwindcss -i assets/styles/tailwind.css -o src/public/static/styles.css

.PHONY: dev
dev:
	docker compose up -d

.PHONY: prod
prod:
	docker compose up -d -f docker-compose.prod.yml

.PHONY: psql
psql:
	docker-compose exec db psql --username=user --dbname=inpv

.PHONY: migrate
migrate:
	docker compose exec web python manage.py migrate

.PHONY: build-validator
build-validator:
	docker build -f Dockerfile-validator -t restricted_python .

.PHONY: lint
lint:
	pylint --rcfile pylintrc.toml src

