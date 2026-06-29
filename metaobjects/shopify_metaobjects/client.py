from dataclasses import is_dataclass
from typing import Any

from shopify_requests.graphql_service import execute_admin_graphql

from .definition import MetaobjectDefinitionSpec, MetaobjectFieldSpec
from .exceptions import DefinitionError, UpsertError
from .metaobject import Metaobject
from .mutations import (
    METAOBJECT_DEFINITION_CREATE,
    METAOBJECT_DEFINITION_UPDATE,
    METAOBJECT_UPDATE,
    METAOBJECT_UPSERT,
)
from .queries import METAOBJECT_BY_HANDLE, METAOBJECT_DEFINITION_BY_TYPE
from .validation import validate_metaobject


def _publishable_active_input(definition: MetaobjectDefinitionSpec | None) -> dict | None:
    if definition is None or not definition.capabilities:
        return None
    publishable = definition.capabilities.get('publishable') or {}
    if not publishable.get('enabled'):
        return None
    return {'publishable': {'status': 'ACTIVE'}}


class MetaobjectClient:
    def __init__(self, shop: str):
        self.shop = shop

    def get_definition(self, type: str) -> MetaobjectDefinitionSpec | None:
        result = execute_admin_graphql(
            METAOBJECT_DEFINITION_BY_TYPE,
            shop=self.shop,
            variables={"type": type},
        )
        if not result.ok:
            raise DefinitionError(
                result.log_detail or "Failed to fetch metaobject definition",
                error_code=result.error_code,
            )
        definition_data = (result.data or {}).get("metaobjectDefinitionByType")
        if not definition_data:
            return None
        return MetaobjectDefinitionSpec.from_dict(definition_data)

    def ensure_definition(
        self, spec: MetaobjectDefinitionSpec
    ) -> MetaobjectDefinitionSpec:
        existing = self.get_definition(spec.type)
        if existing:
            return self.sync_missing_fields(existing, spec)
        return self.create_definition(spec)

    def sync_missing_fields(
        self,
        existing: MetaobjectDefinitionSpec,
        spec: MetaobjectDefinitionSpec,
    ) -> MetaobjectDefinitionSpec:
        existing_keys = {field.key for field in existing.fields}
        missing = [field for field in spec.fields if field.key not in existing_keys]
        if not missing:
            return existing
        if not existing.id:
            raise DefinitionError(
                f"Cannot add fields to {spec.type}: definition id missing from Shopify response"
            )
        return self.add_definition_fields(existing.id, missing)

    def add_definition_fields(
        self,
        definition_id: str,
        fields: list[MetaobjectFieldSpec],
    ) -> MetaobjectDefinitionSpec:
        result = execute_admin_graphql(
            METAOBJECT_DEFINITION_UPDATE,
            shop=self.shop,
            variables={
                "id": definition_id,
                "definition": {
                    "fieldDefinitions": [
                        {"create": field_spec.to_shopify_input()}
                        for field_spec in fields
                    ]
                },
            },
        )
        if not result.ok:
            raise DefinitionError(
                result.log_detail or "Failed to update metaobject definition",
                error_code=result.error_code,
            )
        payload = (result.data or {}).get("metaobjectDefinitionUpdate", {})
        user_errors = payload.get("userErrors") or []
        if user_errors:
            raise DefinitionError(
                "; ".join(error.get("message", str(error)) for error in user_errors),
                user_errors=user_errors,
            )
        definition_data = payload.get("metaobjectDefinition")
        if not definition_data:
            raise DefinitionError("metaobjectDefinitionUpdate returned no definition")
        return MetaobjectDefinitionSpec.from_dict(definition_data)

    def create_definition(
        self, spec: MetaobjectDefinitionSpec
    ) -> MetaobjectDefinitionSpec:
        result = execute_admin_graphql(
            METAOBJECT_DEFINITION_CREATE,
            shop=self.shop,
            variables={"definition": spec.to_shopify_input()},
        )
        if not result.ok:
            raise DefinitionError(
                result.log_detail or "Failed to create metaobject definition",
                error_code=result.error_code,
            )
        payload = (result.data or {}).get("metaobjectDefinitionCreate", {})
        user_errors = payload.get("userErrors") or []
        if user_errors:
            raise DefinitionError(
                "; ".join(error.get("message", str(error)) for error in user_errors),
                user_errors=user_errors,
            )
        definition_data = payload.get("metaobjectDefinition")
        if not definition_data:
            raise DefinitionError("metaobjectDefinitionCreate returned no definition")
        return MetaobjectDefinitionSpec.from_dict(definition_data)

    def get_by_handle(self, type: str, handle: str) -> Metaobject | None:
        result = execute_admin_graphql(
            METAOBJECT_BY_HANDLE,
            shop=self.shop,
            variables={"handle": handle, "type": type},
        )
        if not result.ok:
            raise UpsertError(
                result.log_detail or "Failed to fetch metaobject",
                error_code=result.error_code,
            )
        metaobject_data = (result.data or {}).get("metaobjectByHandle")
        if not metaobject_data:
            return None
        return Metaobject.from_shopify_data(metaobject_data)

    def update(
        self,
        metaobject_id: str,
        metaobject: Metaobject,
        *,
        definition: MetaobjectDefinitionSpec | None = None,
        validate: bool = True,
        redirect_new_handle: bool = True,
    ) -> Metaobject:
        if validate and definition is not None:
            errors = validate_metaobject(metaobject, definition)
            if errors:
                raise UpsertError("; ".join(errors))

        field_types = (
            {field.key: field.type for field in definition.fields}
            if definition is not None
            else {}
        )
        shopify_fields = metaobject.to_shopify_fields(field_types)
        metaobject_input: dict[str, Any] = {
            'handle': metaobject.handle,
            'fields': shopify_fields,
        }
        capabilities = _publishable_active_input(definition)
        if capabilities:
            metaobject_input['capabilities'] = capabilities
        if redirect_new_handle:
            metaobject_input['redirectNewHandle'] = True
        result = execute_admin_graphql(
            METAOBJECT_UPDATE,
            shop=self.shop,
            variables={
                "id": metaobject_id,
                "metaobject": metaobject_input,
            },
        )
        if not result.ok:
            raise UpsertError(
                result.log_detail or "Failed to update metaobject",
                error_code=result.error_code,
            )
        payload = (result.data or {}).get("metaobjectUpdate", {})
        user_errors = payload.get("userErrors") or []
        if user_errors:
            raise UpsertError(
                "; ".join(error.get("message", str(error)) for error in user_errors),
                user_errors=user_errors,
            )
        metaobject_data = payload.get("metaobject")
        if not metaobject_data:
            raise UpsertError("metaobjectUpdate returned no metaobject")
        return Metaobject.from_shopify_data(metaobject_data)

    def upsert(
        self,
        metaobject: Metaobject,
        *,
        definition: MetaobjectDefinitionSpec | None = None,
        validate: bool = True,
    ) -> Metaobject:
        if validate and definition is not None:
            errors = validate_metaobject(metaobject, definition)
            if errors:
                raise UpsertError("; ".join(errors))

        field_types = (
            {field.key: field.type for field in definition.fields}
            if definition is not None
            else {}
        )
        shopify_fields = metaobject.to_shopify_fields(field_types)
        metaobject_input: dict[str, Any] = {'fields': shopify_fields}
        capabilities = _publishable_active_input(definition)
        if capabilities:
            metaobject_input['capabilities'] = capabilities
        variables = {
            "handle": {
                "type": metaobject.type,
                "handle": metaobject.handle,
            },
            "metaobject": metaobject_input,
        }
        result = execute_admin_graphql(
            METAOBJECT_UPSERT,
            shop=self.shop,
            variables=variables,
        )
        if not result.ok:
            raise UpsertError(
                result.log_detail or "Failed to upsert metaobject",
                error_code=result.error_code,
            )
        payload = (result.data or {}).get("metaobjectUpsert", {})
        user_errors = payload.get("userErrors") or []
        if user_errors:
            raise UpsertError(
                "; ".join(error.get("message", str(error)) for error in user_errors),
                user_errors=user_errors,
            )
        metaobject_data = payload.get("metaobject")
        if not metaobject_data:
            raise UpsertError("metaobjectUpsert returned no metaobject")
        return Metaobject.from_shopify_data(metaobject_data)

    def upsert_many(
        self,
        metaobjects: list[Metaobject],
        *,
        definition: MetaobjectDefinitionSpec | None = None,
        validate: bool = True,
    ) -> dict[str, int]:
        stats = {"upserted": 0, "failed": 0}
        for metaobject in metaobjects:
            try:
                self.upsert(metaobject, definition=definition, validate=validate)
                stats["upserted"] += 1
            except UpsertError:
                stats["failed"] += 1
        return stats

    def sync(
        self,
        data: Any,
        *,
        definition: MetaobjectDefinitionSpec,
        ensure_definition: bool = True,
        validate: bool = True,
        existing_id: str | None = None,
    ) -> Metaobject:
        if ensure_definition:
            self.ensure_definition(definition)
        if is_dataclass(data):
            metaobject = Metaobject.from_dataclass(data, type=definition.type)
        elif isinstance(data, dict):
            metaobject = Metaobject.from_dict(data, type=definition.type)
        elif isinstance(data, Metaobject):
            metaobject = data
        else:
            raise TypeError("data must be a dict, dataclass instance, or Metaobject")
        if existing_id:
            return self.update(
                existing_id,
                metaobject,
                definition=definition,
                validate=validate,
            )
        return self.upsert(metaobject, definition=definition, validate=validate)
