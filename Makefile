define USAGE
A small toy API for executing code in isolated environments.

Commands:
	build:   Build docker images.
	up: 	 Run docker container.
	dev:     Run both `build` and `up`.
	test:    Test the code.
endef


export USAGE

help:
	@echo "$$USAGE"

build:
	docker-compose build

up:
	docker-compose up --force-recreate --renew-anon-volumes

dev:
	make build
	make up

pytest:
	docker exec -it cli_api_web_1 pytest $(test_loc)
