from dataclasses import asdict, is_dataclass
from typing import Any, Optional

from .serialization import serialize_field_value


class Metaobject:
    def __init__(
        self,
        type: str,
        handle: str,
        id: Optional[str] = None,
        fields: Optional[dict[str, Any]] = None,
        metafields: Optional[dict[str, dict[str, Any]]] = None,
    ):
        self.id = id
        self.type = type
        self.handle = handle
        self.fields = fields if fields is not None else {}
        self.metafields = metafields if metafields is not None else {}

    @classmethod
    def from_shopify_data(cls, data: dict[str, Any]) -> "Metaobject":
        fields = {item["key"]: item["value"] for item in data.get("fields", [])}
        metafields: dict[str, dict[str, Any]] = {}
        metafield_container = data.get("metafields") or {}
        edges = metafield_container.get("edges", [])
        for edge in edges:
            node = edge.get("node") or edge
            namespace = node.get("namespace", "custom")
            key = node.get("key")
            if namespace not in metafields:
                metafields[namespace] = {}
            metafields[namespace][key] = node
        return cls(
            type=data.get("type"),
            handle=data.get("handle"),
            id=data.get("id"),
            fields=fields,
            metafields=metafields,
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        *,
        type: str,
        handle_key: str = "handle",
    ) -> "Metaobject":
        if handle_key not in data:
            raise ValueError(f"Missing required key '{handle_key}' in data dict")
        handle = str(data[handle_key])
        fields = {
            key: value
            for key, value in data.items()
            if key != handle_key
        }
        return cls(type=type, handle=handle, fields=fields)

    @classmethod
    def from_dataclass(
        cls,
        instance: Any,
        *,
        type: str,
        handle_field: str = "handle",
    ) -> "Metaobject":
        if not is_dataclass(instance):
            raise TypeError(f"{instance!r} is not a dataclass instance")
        return cls.from_dict(asdict(instance), type=type, handle_key=handle_field)

    def to_shopify_fields(self) -> list[dict[str, str]]:
        serialized = []
        for key, value in self.fields.items():
            if isinstance(value, bool):
                serialized.append(
                    {"key": key, "value": serialize_field_value(value, "boolean")}
                )
            elif isinstance(value, (dict, list)):
                serialized.append(
                    {"key": key, "value": serialize_field_value(value, "json")}
                )
            else:
                serialized.append({"key": key, "value": str(value)})
        return serialized

    def get_field(self, key: str) -> Optional[Any]:
        return self.fields.get(key)

    def set_field(self, key: str, value: Any) -> None:
        self.fields[key] = value

    def get_metafield(
        self, key: str, namespace: str = "custom"
    ) -> Optional[dict[str, Any]]:
        return self.metafields.get(namespace, {}).get(key)

    def set_metafield(
        self,
        key: str,
        value: str,
        type: str = "single_line_text_field",
        namespace: str = "custom",
    ) -> None:
        if namespace not in self.metafields:
            self.metafields[namespace] = {}
        self.metafields[namespace][key] = {
            "key": key,
            "value": value,
            "type": type,
            "namespace": namespace,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "handle": self.handle,
            "fields": self.fields,
            "metafields": self.metafields,
        }
