# Shopify Metaobjects Toolkit

A powerful and flexible Python toolkit for managing Shopify Metaobjects via the GraphQL Admin API.

---

## ✨ Features

- **CRUD Operations**: Full support for creating, reading, updating, and deleting (CRUD) both Metaobjects and their Definitions.
- **Batch Processing**: Efficiently load data from CSV files with automatic "upsert" (update or insert) logic based on a unique `handle`.
- **Data Export**: Fetch and export metaobjects to CSV files for backups or analysis.
- **Introspection**: Easily inspect the structure, fields, and validations of any metaobject definition.
- **Resilient**: Automatic retry mechanism for API rate limits and transient network errors.
- **Modular Design**: Clean, package-based structure that is easy to extend and integrate into other projects.
- **Secure**: Uses environment variables to manage sensitive API credentials.

---

## 🚀 Installation

1. **Clone this repository:**
    ```bash
    git clone https://github.com/aavendano/Shopify_Metaobjects.git
    cd Shopify_Metaobjects
    ```

2. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **(Optional) For development, install the package in editable mode:**
    ```bash
    pip install -e .
    ```

---

## 🔑 Configuration

Create a `.env` file in the project root with your Shopify credentials:

```env
SHOPIFY_SHOP_DOMAIN=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_your-admin-api-access-token
```

---

## 📄 CSV File Format

Your CSV file should have a header row with column names that correspond to the fields of your Shopify metaobject.  
**The first column must be named `handle` and will be used as the unique identifier for upsert operations.**

**Example CSV:**
```csv
handle,fabric_name,stretch_level,is_organic
main-cotton,Classic Cotton,2,true
stretch-denim,Stretch Denim,8,false
organic-linen,Organic Linen,1,true
```

---

## 🛠️ Basic Usage

<details>
<summary>Python Example</summary>

```python
from shopify_metaobject_loader import ShopifyMetaobjectLoader

# Initialize the loader
loader = ShopifyMetaobjectLoader(
    shop_domain="your-store.myshopify.com",
    access_token="your-admin-api-access-token"
)

# Process the CSV file
stats = loader.process_csv(
    file_path="data.csv",
    metaobject_type="my_fabric_type"
)

print(f"Created: {stats['created']}")
print(f"Updated: {stats['updated']}")
print(f"Failed: {stats['failed']}")
```
</details>

---

## ▶️ Running as a Script

You can also run the module directly as a script:

```bash
python shopify_metaobject_loader.py
```

> **Note:** Make sure your `.env` file is properly configured before running the script.

---

## ⚠️ Error Handling

The module includes comprehensive error handling for:

- File not found or CSV parsing errors
- Network issues or failed connections to the Shopify API
- GraphQL API errors (invalid permissions, malformed queries, validation errors)

All errors are logged with appropriate context and severity levels.

---

## 📋 Logging

The module uses Python's built-in logging module. Logs include:

- Successful operations (`INFO` level)
- Warnings and non-critical errors (`WARNING` level)
- Critical errors (`ERROR` level)

---

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

## 🧩 Metaobject Type Example: Fabric Type (`my_fabric_type`)

**Description:**  
A type for describing different fabric materials.

### Field Summary

| Field Name    | Key           | Type                   | Required | Description                                 | Validations                |
|---------------|---------------|------------------------|----------|---------------------------------------------|----------------------------|
| Fabric Name   | fabric_name   | single_line_text_field | Yes      | The name of the fabric material             | min_length:2, max_length:100 |
| Stretch Level | stretch_level | number_integer         | Yes      | The stretch level of the fabric (1-10)      | min:1, max:10              |
| Is Organic    | is_organic    | boolean                | No       | Whether the fabric is made from organic materials |                            |
| Handle        | handle        | single_line_text_field | Yes      | The unique identifier for the fabric        | pattern: ^[a-z0-9-]+$      |

- **Total Fields:** 4
- **Required Fields:** 3
- **Optional Fields:** 1

---

## 🧑‍💻 Metaobject Definition Example

<details>
<summary>Python Example</summary>

```python
from shopify_metaobject_loader import ShopifyMetaobjectLoader

# Initialize the loader
loader = ShopifyMetaobjectLoader(
    shop_domain="your-store.myshopify.com",
    access_token="your-access-token"
)

# Define the fields for your metaobject type
fields = [
    {
        "key": "fabric_name",
        "name": "Fabric Name",
        "type": "single_line_text_field",
        "description": "The name of the fabric material",
        "required": True,
        "validations": [
            {"name": "min_length", "value": "2"},
            {"name": "max_length", "value": "100"}
        ]
    },
    {
        "key": "stretch_level",
        "name": "Stretch Level",
        "type": "number_integer",
        "description": "The stretch level of the fabric (1-10)",
        "required": True,
        "validations": [
            {"name": "min", "value": "1"},
            {"name": "max", "value": "10"}
        ]
    },
    {
        "key": "is_organic",
        "name": "Is Organic",
        "type": "boolean",
        "description": "Whether the fabric is made from organic materials",
        "required": False
    },
    {
        "key": "handle",
        "name": "Handle",
        "type": "single_line_text_field",
        "description": "The unique identifier for the fabric",
        "required": True,
        "validations": [
            {"name": "pattern", "value": "^[a-z0-9-]+$"}
        ]
    }
]

# Create the metaobject definition
definition = loader.create_metaobject_definition(
    type_name="my_fabric_type",
    display_name="Fabric Type",
    description="A type for describing different fabric materials",
    fields=fields
)

# Print a human-readable description
loader.print_metaobject_type_description("my_fabric_type")

# Or get the description as a dictionary
description = loader.describe_metaobject_type("my_fabric_type")

# Access specific parts of the description
print(f"Total fields: {description['field_summary']['total_fields']}")
print(f"Required fields: {description['field_summary']['required_fields']}")
print(f"Optional fields: {description['field_summary']['optional_fields']}")

# Get field types summary
for field_type, count in description['field_summary']['field_types'].items():
    print(f"- {field_type}: {count}")

# Access field details
for field in description['fields']['required']:
    print(f"\nField: {field['name']}")
    print(f"Key: {field['key']}")
    print(f"Type: {field['type']}")
    print(f"Description: {field['description']}")
    print("Validations:", field['validations'])
```
</details>
