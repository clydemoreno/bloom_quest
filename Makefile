# Define variables
DOCKER_COMPOSE = docker-compose


# Targets
.PHONY: build up down logs exec

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:

	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f

exec:
	$(DOCKER_COMPOSE) exec python-app /bin/bash

build_db_image:
	docker build -t my-own-mysql -f ./db/Dockerfile

push_to_origin:
	git commit -m "all changes"
	git add .
	git push git@github.com-personal:clydemoreno/bloom_quest.git

prof:
	mprof run ./trial/array_double_buffer.py

flask:
	export FLASK_APP=app.py
	pyenv shell app2 
	flask run

messaging_test:
	python3 -m unittest async_messaging_test.py


# Default target
default: up
