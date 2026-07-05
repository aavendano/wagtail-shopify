"""Tests for export_config registry."""

from django.test import TestCase

from shopify_content.export_config.glossary import glossary_index_consumer
from shopify_content.export_config.location import location_index_consumer
from shopify_content.export_config.registry import (
    get_consumer_for_slug,
    registered_root_slugs,
)


class ExportConfigRegistryTests(TestCase):
    def test_registered_root_slugs(self):
        slugs = registered_root_slugs()
        self.assertIn('glossary', slugs)
        self.assertIn('local-us', slugs)

    def test_get_consumer_for_slug(self):
        self.assertIs(get_consumer_for_slug('glossary'), glossary_index_consumer)
        self.assertIs(get_consumer_for_slug('local-us'), location_index_consumer)
        self.assertIsNone(get_consumer_for_slug('unknown-root'))
