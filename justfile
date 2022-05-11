default: format lint test coverage

alias f := format
alias l := lint
alias t := test
alias c := coverage
alias r := release
alias b := build

# Code Quality
format:
    poetry run black .
    poetry run isort .

lint: format
    poetry run flake8 spidermatch/ tests/

test:
    poetry run pytest

open-in-browser file:
    #!/usr/bin/env python3
    import os, webbrowser, sys
    from urllib.request import pathname2url

    webbrowser.open("file://" + pathname2url(os.path.abspath("{{file}}")))


coverage: && (open-in-browser "htmlcov/index.html")
	poetry run coverage run --source spidermatch -m pytest
	poetry run coverage report -m
	poetry run coverage html

# Building and publishing
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

clean: clean-build clean-pyc clean-test

release: build
	poetry publish

build: clean
	poetry build

bundle: clean
    poetry run pyinstaller --onefile --windowed --noconfirm --add-data spidermatch/windows/:windows/ --add-data spidermatch/assets/:assets/ -i spidermatch/assets/spidermatch.icns --clean --name "SpiderMatch" spidermatch/main.py
