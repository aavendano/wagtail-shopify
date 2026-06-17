# Shopify Metaobjects Toolkit

Modular Python toolkit for managing Shopify Metaobjects via the Admin GraphQL API. Integrated with the wagtail-shopify project through `shopify_requests.execute_admin_graphql`.

---

## Features

- **Definition management**: Create and fetch metaobject type definitions
- **Instance upsert**: Create or update metaobjects by `handle`
- **Dict and dataclass input**: Build definitions and instances from Python data structures
- **Validation**: Optional pre-flight validation against a definition before upsert
- **Modular package**: [`metaobjects/shopify_metaobjects/`](metaobjects/shopify_metaobjects/)

---

## Configuration

The client uses the same shop token flow as the rest of the project (`ShopConfig` + `execute_admin_graphql`). Pass the shop domain explicitly:

```python
shop = "your-store.myshopify.com"
client = MetaobjectClient(shop)
```

Ensure the app is installed on the shop and has the required Admin API scopes for metaobjects.

---

## Basic usage

### From a dataclass

```python
from dataclasses import dataclass

from metaobjects import Metaobject, MetaobjectClient, MetaobjectDefinitionSpec

@dataclass
class FabricSpec:
    handle: str
    fabric_name: str
    stretch_level: int
    is_organic: bool

shop = "your-store.myshopify.com"
client = MetaobjectClient(shop)

definition = MetaobjectDefinitionSpec.from_dataclass(
    FabricSpec,
    type="fabric",
    name="Fabric",
    description="Fabric material specifications",
)
client.ensure_definition(definition)

instance = Metaobject.from_dataclass(
    FabricSpec("main-cotton", "Classic Cotton", 2, True),
    type="fabric",
)
client.upsert(instance, definition=definition)
```

### One-shot sync

```python
client.sync(
    FabricSpec("main-cotton", "Classic Cotton", 2, True),
    definition=definition,
)
```

### From a dict

```python
data = {
    "handle": "main-cotton",
    "fabric_name": "Classic Cotton",
    "stretch_level": 2,
    "is_organic": True,
}
instance = Metaobject.from_dict(data, type="fabric")
client.upsert(instance)
```

---

## Package structure

```
metaobjects/
  shopify_metaobjects/
    client.py          # MetaobjectClient
    definition.py      # MetaobjectDefinitionSpec, MetaobjectFieldSpec
    metaobject.py      # Metaobject
    serialization.py   # Python type → Shopify field type mapping
    mutations.py       # GraphQL mutations
    queries.py         # GraphQL queries
    validation.py      # Pre-upsert validation
    exceptions.py      # MetaobjectError, DefinitionError, UpsertError
```

---

## Custom Shopify field types

Override inferred types with dataclass field metadata:

```python
from dataclasses import dataclass, field

@dataclass
class ArticleTeaser:
    handle: str
    body: str = field(metadata={"shopify_type": "multi_line_text_field"})
```

---

## Error handling

- `DefinitionError`: definition fetch/create failed
- `UpsertError`: upsert failed (API error or userErrors)
- Both expose `.error_code` and `.user_errors` when available

---

## Tests

```bash
python manage.py test metaobjects.shopify_metaobjects.tests
```

---

## API reference

See [`docs/Documentation.txt`](docs/Documentation.txt) for detailed method documentation.
