SHELL := /bin/bash
.PHONY: help build-docs deploy-docs format install lint test build release

help:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

build-docs:
	cd docs && poetry run make clean html

deploy-docs:
	make build-docs
	poetry run ghp-import -n -p docs/build/html/

format:
	poetry run isort --profile black .
	poetry run black .

install:
	poetry install

lint:
	poetry run isort --profile black -c --diff .
	poetry run black --check .
	poetry run flake8 .

test:
	poetry run pytest --cov=stage_left --cov-report term --cov-report xml ./tests

build:
	poetry build

release:
	# usage: `make release version=0.0.0`
	make test
	@echo ""
	make lint
	@echo ""
	./release.sh "$(version)"
