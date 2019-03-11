PY?=python3
MINIMALOYTHONVERSION=3.3

help:
	@echo 'Makefile for a webservice                                                      '
	@echo '                                                                               '
	@echo 'Usage:                                                                         '
	@echo '   make setup                             setup project                        '
	@echo '   make serve [HOST=127.0.0.1 PORT=8000] serve service at http://127.0.0.1:8000'

test_python_version:
    @./scripts/verify_python.sh $(MINIMALPYTHONVERSION) || (echo "Please install python version not older than $(MINIMALPYTHONVERSION)" && exit 1)

setup: test_python_version
    @python -m venv ./ && pip install -r requirements.txt

serve:
    gunicorn -b 127.0.0.1:8000 app

.PHONY: setup serve test_python_version