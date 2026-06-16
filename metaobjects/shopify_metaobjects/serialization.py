import json
from dataclasses import MISSING, fields as dataclass_fields, is_dataclass
from typing import Any, Union, get_args, get_origin

PYTHON_TO_SHOPIFY_TYPE = {
    str: "single_line_text_field",
    int: "number_integer",
    float: "number_decimal",
    bool: "boolean",
    dict: "json",
    list: "json",
}


def resolve_python_type(annotation: Any) -> type:
    """Resolve Optional[T] and bare annotations to a concrete type."""
    origin = get_origin(annotation)
    if origin is Union:
        args = [arg for arg in get_args(annotation) if arg is not type(None)]
        if args:
            return args[0]
    if isinstance(annotation, type):
        return annotation
    return str


def infer_shopify_type(python_type: type, metadata: dict | None = None) -> str:
    if metadata and "shopify_type" in metadata:
        return metadata["shopify_type"]
    return PYTHON_TO_SHOPIFY_TYPE.get(python_type, "single_line_text_field")


def serialize_field_value(value: Any, shopify_type: str) -> str:
    if shopify_type == "boolean":
        return "true" if value else "false"
    if shopify_type == "json":
        return json.dumps(value)
    return str(value)


def field_specs_from_dataclass(
    dc_type: type,
    *,
    handle_field: str = "handle",
) -> list[dict[str, Any]]:
    if not is_dataclass(dc_type):
        raise TypeError(f"{dc_type!r} is not a dataclass")

    specs = []
    for dc_field in dataclass_fields(dc_type):
        if dc_field.name == handle_field:
            continue
        python_type = resolve_python_type(dc_field.type)
        shopify_type = infer_shopify_type(python_type, dc_field.metadata)
        required = dc_field.default is MISSING and dc_field.default_factory is MISSING
        specs.append(
            {
                "key": dc_field.name,
                "name": dc_field.metadata.get(
                    "name", dc_field.name.replace("_", " ").title()
                ),
                "type": shopify_type,
                "description": dc_field.metadata.get("description", ""),
                "required": required,
                "validations": list(dc_field.metadata.get("validations", [])),
            }
        )
    return specs
