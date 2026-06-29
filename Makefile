.PHONY: test test-glossary install-test-deps

VENV_PYTHON := .venv/bin/python
PYTEST := $(VENV_PYTHON) -m pytest

test:
	$(PYTEST)

test-glossary:
	$(PYTEST) shopify_content/tests/test_glossary.py metaobjects/shopify_metaobjects/tests/test_client.py

install-test-deps:
	$(VENV_PYTHON) -m pip install -r requirements.txt
