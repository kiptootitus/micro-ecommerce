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

update_all: migrations migrate runserver