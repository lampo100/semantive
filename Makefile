VENV = .venv
HOST=localhost
PORT=5000
export VIRTUAL_ENV := $(abspath ${VENV})
export PATH := ${VIRTUAL_ENV}/bin:${PATH}
.PHONY: python-reqs setup serve test

help:
	@echo 'Makefile for a webservice                                                      '
	@echo '                                                                               '
	@echo 'Usage:                                                                         '
	@echo '   make setup                             setup project                        '
	@echo '   make serve [HOST=127.0.0.1 PORT=8000] serve service at http://127.0.0.1:8000'

${VENV}:
	python3 -m venv $@

python-reqs: requirements.txt | ${VENV}
	pip install --upgrade -r requirements.txt

setup: ${VENV} python-reqs test

serve:
	@gunicorn -b ${HOST}:${PORT} app:app

test:
	@python3 -m unittest tests/test_app.py

