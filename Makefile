.PHONY: install-requirements
install-requirements:
	venv/bin/pip install -r requirements.txt

.PHONY: static
static:
	python ./src/manage.py collectstatic

.PHONY: run-server
run:
	python ./src/manage.py runserver

.PHONY: assets
dev:
	npx tailwindcss -i  src/public/static/input.css -o src/public/static/output.css -w

