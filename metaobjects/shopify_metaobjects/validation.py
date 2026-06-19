import re
from typing import Any

from .definition import MetaobjectDefinitionSpec
from .metaobject import Metaobject

SHOPIFY_TYPE_TO_PYTHON = {
    "single_line_text_field": str,
    "rich_text_field": str,
    "number_integer": int,
    "number_decimal": (int, float),
    "boolean": bool,
    "date": str,
    "date_time": str,
    "json": (dict, list),
    "color": str,
    "rating": (int, float),
    "dimension": (int, float),
    "volume": (int, float),
    "weight": (int, float),
}


def validate_field_type(value: Any, expected_type: str) -> bool:
    expected = SHOPIFY_TYPE_TO_PYTHON.get(expected_type)
    if not expected:
        return True
    return isinstance(value, expected)


def validate_field_value(value: Any, validation: dict[str, Any]) -> bool:
    name = validation["name"]
    rule_value = validation["value"]

    if name == "min":
        return float(value) >= float(rule_value)
    if name == "max":
        return float(value) <= float(rule_value)
    if name == "pattern":
        return bool(re.match(rule_value, str(value)))
    if name == "in":
        return value in rule_value.split(",")
    return True


def validate_metaobject(
    metaobject: Metaobject,
    definition: MetaobjectDefinitionSpec,
) -> list[str]:
    errors: list[str] = []

    for field_spec in definition.fields:
        if field_spec.required and field_spec.key not in metaobject.fields:
            errors.append(f"Missing required field: {field_spec.key}")

    for field_spec in definition.fields:
        if field_spec.key not in metaobject.fields:
            continue
        value = metaobject.fields[field_spec.key]
        if not validate_field_type(value, field_spec.type):
            errors.append(
                f"Invalid type for field {field_spec.key}: "
                f"expected {field_spec.type}, got {type(value).__name__}"
            )
        for validation in field_spec.validations:
            if not validate_field_value(value, validation):
                errors.append(
                    f"Validation failed for field {field_spec.key}: "
                    f"{validation['name']} = {validation['value']}"
                )

    return errors
