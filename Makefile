define USAGE
A small toy API for executing code in isolated environments.

Commands:
	build:     Build docker images.
	up: 	   Run docker container.
	dev:       Run both `build` and `up`.
	pytest:    Test the code.
        ssh:       SSH into the web container.
endef


export USAGE

help:
	@echo "$$USAGE"

build:
	docker-compose build

up:
	docker-compose up --force-recreate --renew-anon-volumes

up-detached:
	docker-compose up --force-recreate --renew-anon-volumes -d

dev:
	make build
	make up

dev-detached:
	make build
	make up-detached

pytest:
	docker exec cli_api_web_1 pytest $(test_loc)

pytest-cov:
	docker exec cli_api_web_1 pytest --cov-report xml:cov.xml --cov=cli_api tests/
	docker cp cli_api_web_1:/app/cov.xml .

ssh:
	docker exec -it cli_api_web_1 /bin/bash
