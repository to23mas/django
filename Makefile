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

.PHONY: prod-up
prod-up:
	docker compose -f docker-compose.prod.yml up -d

.PHONY: prod-up-build
prod-up-build:
	docker compose -f docker-compose.prod.yml up -d --build

.PHONY: prod-down
prod-down:
	docker compose -f docker-compose.prod.yml down --remove-orphans

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

.PHONY: inttest
inttest: dev
	docker compose exec -e PYTHONPATH=/usr/src/app web python manage.py test domain.tests.inttest.test_course_storage domain.tests.inttest.test_blockly_storage domain.tests.inttest.test_cli_storage domain.tests.inttest.test_demo_storage domain.tests.inttest.test_lesson_storage domain.tests.inttest.test_project_storage domain.tests.inttest.test_test_storage --keepdb

.PHONY: unittest
unittest: dev
	docker compose exec -e PYTHONPATH=/usr/src/app web python manage.py test domain.tests.unittest.test_blockly domain.tests.unittest.test_chapters domain.tests.unittest.test_clis domain.tests.unittest.test_demos domain.tests.unittest.test_lessons domain.tests.unittest.test_projects domain.tests.unittest.test_tests --keepdb

PHONY: test
test: inttest unittest
