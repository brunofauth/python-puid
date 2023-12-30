.PHONY: edit test lint build

edit:
	@find src/puid -type f -name *.py | xargs --open-tty poetry run vim -p

test:
	@poetry run pytest tests/

lint:
	@poetry run mypy src/puid
	@poetry run mypy tests

build:
	make lint
	make test
	poetry build --format=sdist

