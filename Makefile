.PHONY: test lint build

test:
	@poetry run pytest tests/

lint:
	@poetry run mypy src/puid

build:
	make lint
	make test
	poetry build --format=sdist
