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
	git push git@github.com-personal:clydemoreno/bloom_quest.git

prof:
	mprof run ./trial/array_double_buffer.py

flask:
	export FLASK_APP=grpc_app
	flask run

messaging_test:
	python3 -m unittest async_messaging_test.py

test:
	pytest .

loadtest:
	k6 run ./trial/e2e/loadtest.js

loadtest_with_bloom:
	k6 run ./trial/e2e/test_with_bloom.js

loadtest_without_bloom:
	k6 run ./trial/e2e/test_without_bloom.js

loadtest_with_bloom_threshold:
	k6 run ./trial/e2e/test_with_bloom_threshold.js

loadtest_without_bloom_threshold:
	k6 run ./trial/e2e/test_without_bloom_threshold.js


loadtest_with_bloom_breaking_point:
	k6 run ./trial/e2e/test_with_bloom_breaking_point.js

loadtest_without_bloom_breaking_point:
	k6 run ./trial/e2e/test_without_bloom_breaking_point.js



# Default target
default: up
