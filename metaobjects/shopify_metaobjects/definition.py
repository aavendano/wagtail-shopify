import json
from dataclasses import dataclass, field
from typing import Any, Self

from .serialization import field_specs_from_dataclass

_glossary_definition_gid_cache: dict[str, str | None] = {}


@dataclass
class MetaobjectFieldSpec:
    key: str
    name: str
    type: str
    description: str = ""
    required: bool = False
    validations: list[dict[str, Any]] = field(default_factory=list)

    def to_shopify_input(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "key": self.key,
            "name": self.name,
            "type": self.type,
            "required": self.required,
        }
        if self.description:
            payload["description"] = self.description
        if self.validations:
            payload["validations"] = [
                {
                    "name": validation["name"],
                    "value": (
                        validation["value"]
                        if isinstance(validation.get("value"), str)
                        else json.dumps(validation["value"])
                    ),
                }
                for validation in self.validations
            ]
        return payload


@dataclass
class MetaobjectDefinitionSpec:
    type: str
    name: str
    description: str
    fields: list[MetaobjectFieldSpec]
    id: str | None = None
    display_name_field: str | None = None
    capabilities: dict | None = None
    access: dict | None = None

    def to_shopify_input(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "fieldDefinitions": [
                field_spec.to_shopify_input() for field_spec in self.fields
            ],
        }
        if self.display_name_field:
            payload["displayNameKey"] = self.display_name_field
        if self.capabilities:
            payload["capabilities"] = self._normalize_capabilities(self.capabilities)
        if self.access:
            payload["access"] = self.access
        return payload

    @staticmethod
    def _normalize_capabilities(capabilities: dict) -> dict:
        caps = dict(capabilities)
        renderable = caps.get("renderable")
        if not isinstance(renderable, dict):
            return caps
        data = renderable.get("data")
        if not isinstance(data, dict):
            return caps
        normalized = dict(data)
        if "metaTitleField" in normalized and "metaTitleKey" not in normalized:
            normalized["metaTitleKey"] = normalized.pop("metaTitleField")
        if "metaDescriptionField" in normalized and "metaDescriptionKey" not in normalized:
            normalized["metaDescriptionKey"] = normalized.pop("metaDescriptionField")
        return {**caps, "renderable": {**renderable, "data": normalized}}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        raw_fields = data.get("fields") or data.get("fieldDefinitions") or []
        fields = []
        for raw in raw_fields:
            field_type = raw.get("type")
            if isinstance(field_type, dict):
                field_type = field_type.get("name", "single_line_text_field")
            fields.append(
                MetaobjectFieldSpec(
                    key=raw["key"],
                    name=raw.get("name", raw["key"]),
                    type=field_type or "single_line_text_field",
                    description=raw.get("description") or "",
                    required=bool(raw.get("required", False)),
                    validations=list(raw.get("validations") or []),
                )
            )
        return cls(
            id=data.get("id"),
            type=data["type"],
            name=data.get("name", data["type"]),
            description=data.get("description") or "",
            fields=fields,
        )

    @classmethod
    def glossary_native_reference_fields(
        cls, glossary_definition_gid: str | None = None
    ) -> list['MetaobjectFieldSpec']:
        fields = [
            MetaobjectFieldSpec(
                key='related_products',
                name='Related Products',
                type='list.product_reference',
            ),
            MetaobjectFieldSpec(
                key='related_collections',
                name='Related Collections',
                type='list.collection_reference',
            ),
            MetaobjectFieldSpec(
                key='related_articles',
                name='Related Articles',
                type='list.article_reference',
            ),
        ]
        if glossary_definition_gid:
            fields.append(
                MetaobjectFieldSpec(
                    key='related_glossary_terms',
                    name='Related Glossary Terms',
                    type='list.metaobject_reference',
                    validations=[
                        {
                            'name': 'metaobject_definition_id',
                            'value': glossary_definition_gid,
                        },
                    ],
                ),
            )
        return fields

    @classmethod
    def from_dataclass(
        cls,
        dc_type: type,
        *,
        type: str,
        name: str,
        description: str,
        handle_field: str = "handle",
    ) -> Self:
        specs = field_specs_from_dataclass(dc_type, handle_field=handle_field)
        return cls(
            type=type,
            name=name,
            description=description,
            fields=[MetaobjectFieldSpec(**spec) for spec in specs],
        )


def glossary_definition_gid(shop: str) -> str | None:
    """Cached lookup of glossary_term metaobject definition GID for reference validations."""
    if shop in _glossary_definition_gid_cache:
        return _glossary_definition_gid_cache[shop]

    from .client import MetaobjectClient

    try:
        definition = MetaobjectClient(shop=shop).get_definition('glossary_term')
    except Exception:
        _glossary_definition_gid_cache[shop] = None
        return None

    gid = definition.id if definition else None
    _glossary_definition_gid_cache[shop] = gid
    return gid


def clear_glossary_definition_gid_cache() -> None:
    _glossary_definition_gid_cache.clear()
