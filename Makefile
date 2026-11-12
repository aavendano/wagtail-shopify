.PHONY: test test-glossary install-test-deps devenv-env cms-ui-build

VENV_PYTHON := .venv/bin/python
PYTEST := $(VENV_PYTHON) -m pytest
DEVENV := $(HOME)/Documents/Proyectos/playlovetoys/plt-devenv/bin/devenv

# Render the dev .env (mode 600, gitignored) from the plt-devenv vault. Used by launch.json envFile.
devenv-env:
	$(DEVENV) render wagtail-shopify --out .env

test:
	$(PYTEST)

test-glossary:
	$(PYTEST) shopify_content/tests/test_glossary.py metaobjects/shopify_metaobjects/tests/test_client.py

install-test-deps:
	$(VENV_PYTHON) -m pip install -r requirements.txt

cms-ui-build:
	./bin/build_cms_ui.sh
