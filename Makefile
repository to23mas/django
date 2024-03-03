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
	npx tailwindcss -i assets/styles/tailwind.css -o src/public/static/styles.css -w

.PHONY: dev
dev:
	docker compose up -d

.PHONY: prod
prod:
	docker compose up -d -f docker-compose.prod.yml

