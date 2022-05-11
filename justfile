default: format lint test coverage

alias f := format
alias l := lint
alias t := test
alias c := coverage
alias r := release
alias b := build

os_family := os_family()
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

# Use the OS specific delimiters for paths in PyInstaller
windows_path := if os_family == "windows" { "spidermatch/windows/;windows/" } else { "spidermatch/windows/:windows/" }
assets_path := if os_family == "windows" { "spidermatch/assets/;assets/" } else { "spidermatch/assets/:assets/" }

bundle: clean
    poetry run pyinstaller --onefile --windowed --noconfirm --add-data {{ windows_path }} --add-data {{ assets_path }} -i spidermatch/assets/spidermatch.icns --clean --name "SpiderMatch" spidermatch/main.py
