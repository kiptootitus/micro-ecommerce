.PHONY: runserver
runserver:
	python3 images/garage_backend/manage.py runserver

.PHONY: migrations
migrations:
	python3 images/garage_backend/manage.py makemigrations

.PHONY: migrate
migrate:
	python3 images/garage_backend/manage.py migrate

.PHONY: create_superuser
create_superuser:
	python3 images/garage_backend/manage.py createsuperuser

.PHONY: install
install:
	pip install -r images/garage_backend/requirements.txt

update_all: migrations migrate runserver



# docker commands

docker_run:
	docker run -d -p 8000:8000 images/garage_backend
.PHONY: docker_build
docker_build:
	docker build -t images/garage_backend -f images/garage_backend/Dockerfile images/garage_backend