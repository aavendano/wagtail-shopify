from dataclasses import dataclass
from types import SimpleNamespace
from unittest.mock import patch
import json

from django.test import TestCase

from metaobjects.shopify_metaobjects.client import MetaobjectClient
from metaobjects.shopify_metaobjects.definition import MetaobjectDefinitionSpec, MetaobjectFieldSpec
from metaobjects.shopify_metaobjects.exceptions import UpsertError
from metaobjects.shopify_metaobjects.metaobject import Metaobject
from metaobjects.shopify_metaobjects.serialization import html_to_shopify_rich_text
from shopify_requests.graphql_service import AdminGraphqlResult


@dataclass
class FabricSpec:
    handle: str
    fabric_name: str
    stretch_level: int
    is_organic: bool


def _ok_result(data):
    return AdminGraphqlResult(
        ok=True,
        shop="test-shop.myshopify.com",
        data=data,
        extensions=None,
        error_code=None,
        log_detail="ok",
        reauthorization_required=False,
        retryable=False,
        raw=SimpleNamespace(),
    )


class MetaobjectSerializationTests(TestCase):
    def test_from_dict_extracts_handle_and_fields(self):
        metaobject = Metaobject.from_dict(
            {
                "handle": "main-cotton",
                "fabric_name": "Classic Cotton",
                "stretch_level": 2,
            },
            type="fabric",
        )
        self.assertEqual(metaobject.handle, "main-cotton")
        self.assertEqual(metaobject.type, "fabric")
        self.assertEqual(metaobject.fields["fabric_name"], "Classic Cotton")
        self.assertNotIn("handle", metaobject.fields)

    def test_from_dataclass(self):
        metaobject = Metaobject.from_dataclass(
            FabricSpec("main-cotton", "Classic Cotton", 2, True),
            type="fabric",
        )
        self.assertEqual(metaobject.handle, "main-cotton")
        self.assertTrue(metaobject.fields["is_organic"])

    def test_to_shopify_fields_serializes_bool_and_json(self):
        metaobject = Metaobject(
            type="fabric",
            handle="x",
            fields={"is_organic": True, "meta": {"a": 1}},
        )
        fields = {item["key"]: item["value"] for item in metaobject.to_shopify_fields()}
        self.assertEqual(fields["is_organic"], "true")
        self.assertEqual(fields["meta"], '{"a": 1}')

    def test_to_shopify_fields_serializes_rich_text_html(self):
        metaobject = Metaobject(
            type="location_page",
            handle="x",
            fields={"intro": "<p>Hello <strong>world</strong></p>"},
        )
        field_types = {"intro": "rich_text_field"}
        fields = {item["key"]: item["value"] for item in metaobject.to_shopify_fields(field_types)}
        parsed = json.loads(fields["intro"])
        self.assertEqual(parsed["type"], "root")
        self.assertEqual(parsed["children"][0]["type"], "paragraph")

    def test_html_to_shopify_rich_text_converts_paragraph(self):
        doc = html_to_shopify_rich_text("<p>Hello</p>")
        self.assertEqual(doc["type"], "root")
        self.assertEqual(doc["children"][0]["children"][0]["value"], "Hello")

    def test_from_shopify_data_parses_metafield_edges(self):
        metaobject = Metaobject.from_shopify_data(
            {
                "id": "gid://shopify/Metaobject/1",
                "type": "fabric",
                "handle": "main-cotton",
                "fields": [{"key": "fabric_name", "value": "Cotton"}],
                "metafields": {
                    "edges": [
                        {
                            "node": {
                                "id": "gid://shopify/Metafield/1",
                                "namespace": "custom",
                                "key": "source",
                                "value": "wagtail",
                                "type": "single_line_text_field",
                            }
                        }
                    ]
                },
            }
        )
        self.assertEqual(metaobject.fields["fabric_name"], "Cotton")
        self.assertEqual(metaobject.get_metafield("source")["value"], "wagtail")


class MetaobjectDefinitionSpecTests(TestCase):
    def test_to_shopify_input_uses_admin_api_field_names(self):
        definition = MetaobjectDefinitionSpec(
            type="location_page",
            name="Location Page",
            description="Test",
            display_name_field="titulo",
            capabilities={
                "renderable": {
                    "enabled": True,
                    "data": {
                        "metaTitleField": "titulo",
                        "metaDescriptionField": "subtitulo",
                    },
                },
            },
            fields=[
                MetaobjectFieldSpec(
                    key="titulo",
                    name="Título",
                    type="single_line_text_field",
                    required=True,
                ),
            ],
        )
        payload = definition.to_shopify_input()
        self.assertIn("fieldDefinitions", payload)
        self.assertNotIn("fields", payload)
        self.assertEqual(payload["displayNameKey"], "titulo")
        self.assertNotIn("displayNameField", payload)
        renderable_data = payload["capabilities"]["renderable"]["data"]
        self.assertEqual(renderable_data["metaTitleKey"], "titulo")
        self.assertEqual(renderable_data["metaDescriptionKey"], "subtitulo")

    def test_from_dataclass_excludes_handle(self):
        definition = MetaobjectDefinitionSpec.from_dataclass(
            FabricSpec,
            type="fabric",
            name="Fabric",
            description="Fabric specs",
        )
        keys = {field.key for field in definition.fields}
        self.assertNotIn("handle", keys)
        self.assertIn("fabric_name", keys)
        self.assertEqual(definition.fields[0].type, "single_line_text_field")


class MetaobjectClientTests(TestCase):
    @patch("metaobjects.shopify_metaobjects.client.execute_admin_graphql")
    def test_ensure_definition_returns_existing(self, mock_execute):
        mock_execute.return_value = _ok_result(
            {
                "metaobjectDefinitionByType": {
                    "type": "fabric",
                    "name": "Fabric",
                    "description": "Existing",
                    "fieldDefinitions": [],
                }
            }
        )
        client = MetaobjectClient("test-shop.myshopify.com")
        spec = MetaobjectDefinitionSpec(
            type="fabric",
            name="Fabric",
            description="New",
            fields=[],
        )
        result = client.ensure_definition(spec)
        self.assertEqual(result.name, "Fabric")
        mock_execute.assert_called_once()

    @patch("metaobjects.shopify_metaobjects.client.execute_admin_graphql")
    def test_ensure_definition_creates_when_missing(self, mock_execute):
        mock_execute.side_effect = [
            _ok_result({"metaobjectDefinitionByType": None}),
            _ok_result(
                {
                    "metaobjectDefinitionCreate": {
                        "metaobjectDefinition": {
                            "type": "fabric",
                            "name": "Fabric",
                            "description": "New",
                            "fieldDefinitions": [
                                {
                                    "key": "fabric_name",
                                    "name": "Fabric Name",
                                    "required": True,
                                    "type": {"name": "single_line_text_field"},
                                    "validations": [],
                                },
                                {
                                    "key": "stretch_level",
                                    "name": "Stretch Level",
                                    "required": True,
                                    "type": {"name": "number_integer"},
                                    "validations": [],
                                },
                                {
                                    "key": "is_organic",
                                    "name": "Is Organic",
                                    "required": True,
                                    "type": {"name": "boolean"},
                                    "validations": [],
                                },
                            ],
                        },
                        "userErrors": [],
                    }
                }
            ),
        ]
        client = MetaobjectClient("test-shop.myshopify.com")
        spec = MetaobjectDefinitionSpec.from_dataclass(
            FabricSpec,
            type="fabric",
            name="Fabric",
            description="New",
        )
        result = client.ensure_definition(spec)
        self.assertEqual(result.type, "fabric")
        self.assertEqual(len(result.fields), 3)
        self.assertEqual(mock_execute.call_count, 2)

    @patch("metaobjects.shopify_metaobjects.client.execute_admin_graphql")
    def test_upsert_success(self, mock_execute):
        mock_execute.return_value = _ok_result(
            {
                "metaobjectUpsert": {
                    "metaobject": {
                        "id": "gid://shopify/Metaobject/1",
                        "type": "fabric",
                        "handle": "main-cotton",
                        "fields": [{"key": "fabric_name", "value": "Cotton"}],
                        "metafields": {"edges": []},
                    },
                    "userErrors": [],
                }
            }
        )
        client = MetaobjectClient("test-shop.myshopify.com")
        metaobject = Metaobject(
            type="fabric",
            handle="main-cotton",
            fields={"fabric_name": "Cotton"},
        )
        result = client.upsert(metaobject, validate=False)
        self.assertEqual(result.id, "gid://shopify/Metaobject/1")

    @patch("metaobjects.shopify_metaobjects.client.execute_admin_graphql")
    def test_upsert_raises_on_user_errors(self, mock_execute):
        mock_execute.return_value = _ok_result(
            {
                "metaobjectUpsert": {
                    "metaobject": None,
                    "userErrors": [{"field": ["handle"], "message": "Invalid handle"}],
                }
            }
        )
        client = MetaobjectClient("test-shop.myshopify.com")
        metaobject = Metaobject(type="fabric", handle="bad handle", fields={})
        with self.assertRaises(UpsertError):
            client.upsert(metaobject, validate=False)

    @patch("metaobjects.shopify_metaobjects.client.execute_admin_graphql")
    def test_sync_end_to_end(self, mock_execute):
        mock_execute.side_effect = [
            _ok_result({"metaobjectDefinitionByType": None}),
            _ok_result(
                {
                    "metaobjectDefinitionCreate": {
                        "metaobjectDefinition": {
                            "type": "fabric",
                            "name": "Fabric",
                            "description": "New",
                            "fieldDefinitions": [
                                {
                                    "key": "fabric_name",
                                    "name": "Fabric Name",
                                    "required": True,
                                    "type": {"name": "single_line_text_field"},
                                    "validations": [],
                                },
                                {
                                    "key": "stretch_level",
                                    "name": "Stretch Level",
                                    "required": True,
                                    "type": {"name": "number_integer"},
                                    "validations": [],
                                },
                                {
                                    "key": "is_organic",
                                    "name": "Is Organic",
                                    "required": True,
                                    "type": {"name": "boolean"},
                                    "validations": [],
                                },
                            ],
                        },
                        "userErrors": [],
                    }
                }
            ),
            _ok_result(
                {
                    "metaobjectUpsert": {
                        "metaobject": {
                            "id": "gid://shopify/Metaobject/1",
                            "type": "fabric",
                            "handle": "main-cotton",
                            "fields": [
                                {"key": "fabric_name", "value": "Classic Cotton"},
                                {"key": "stretch_level", "value": "2"},
                                {"key": "is_organic", "value": "true"},
                            ],
                            "metafields": {"edges": []},
                        },
                        "userErrors": [],
                    }
                }
            ),
        ]
        client = MetaobjectClient("test-shop.myshopify.com")
        definition = MetaobjectDefinitionSpec.from_dataclass(
            FabricSpec,
            type="fabric",
            name="Fabric",
            description="New",
        )
        result = client.sync(
            FabricSpec("main-cotton", "Classic Cotton", 2, True),
            definition=definition,
        )
        self.assertEqual(result.handle, "main-cotton")
        self.assertEqual(mock_execute.call_count, 3)
