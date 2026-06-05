# Metaobject data structure and helpers
from typing import Optional, Dict, Any, List

class Metaobject:
    def __init__(
        self,
        type: str,
        handle: str,
        id: Optional[str] = None,
        fields: Optional[Dict[str, Any]] = None,
        metafields: Optional[Dict[str, Dict[str, Any]]] = None
    ):
        self.id = id
        self.type = type
        self.handle = handle
        self.fields = fields if fields is not None else {}
        self.metafields = metafields if metafields is not None else {}

    @classmethod
    def from_shopify_data(cls, data: Dict[str, Any]) -> 'Metaobject':
        id = data.get('id')
        type_ = data.get('type')
        handle = data.get('handle')
        fields = {f['key']: f['value'] for f in data.get('fields', [])}
        metafields = {}
        for m in data.get('metafields', []):
            ns = m.get('namespace', 'custom')
            key = m.get('key')
            if ns not in metafields:
                metafields[ns] = {}
            metafields[ns][key] = m
        return cls(type=type_, handle=handle, id=id, fields=fields, metafields=metafields)

    def to_shopify_fields(self) -> List[Dict[str, str]]:
        return [{"key": k, "value": str(v)} for k, v in self.fields.items()]

    def get_field(self, key: str) -> Optional[Any]:
        return self.fields.get(key)

    def set_field(self, key: str, value: Any) -> None:
        self.fields[key] = value

    def get_metafield(self, key: str, namespace: str = "custom") -> Optional[Dict[str, Any]]:
        return self.metafields.get(namespace, {}).get(key)

    def set_metafield(self, key: str, value: str, type: str = "single_line_text_field", namespace: str = "custom") -> None:
        if namespace not in self.metafields:
            self.metafields[namespace] = {}
        self.metafields[namespace][key] = {
            "key": key,
            "value": value,
            "type": type,
            "namespace": namespace
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "handle": self.handle,
            "fields": self.fields,
            "metafields": self.metafields
        }
