SHELL := /bin/bash

create_environment:
	python3 -m venv env-africanlibraries

delete_environment:
	rm -rf env-africanlibraries

install:
	pip install --upgrade pip
	pip install -r requirements.txt

initialize:
	python manage.py migrate
	python manage.py initDataLocations
	python manage.py importBooks2 Data_Detailed.xlsx covers 0 250 1
	python manage.py importBooks2 Data_Detailed.xlsx covers 0 250 2
	python manage.py demoUser
	python manage.py createsuperuser

run:
	python manage.py runserver

migration:
	python manage.py makemigrations

migrate:
	python manage.py migrate
