.PHONY: test test-glossary install-test-deps admin-theme admin-theme-check

VENV_PYTHON := .venv/bin/python
PYTEST := $(VENV_PYTHON) -m pytest

test:
	$(PYTEST)

test-glossary:
	$(PYTEST) shopify_content/tests/test_glossary.py metaobjects/shopify_metaobjects/tests/test_client.py

install-test-deps:
	$(VENV_PYTHON) -m pip install -r requirements.txt

# Regenerate the Wagtail admin stylesheet from plt-design-system tokens.
DESIGN_SYSTEM ?= ../plt-design-system

admin-theme:
	python3 scripts/build_admin_theme.py --design-system $(DESIGN_SYSTEM)

admin-theme-check:
	python3 scripts/build_admin_theme.py --design-system $(DESIGN_SYSTEM) --check
