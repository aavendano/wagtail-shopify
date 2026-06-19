import json
import re
from dataclasses import MISSING, fields as dataclass_fields, is_dataclass
from html.parser import HTMLParser
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
    if shopify_type == "rich_text_field":
        if isinstance(value, dict):
            return json.dumps(value)
        return json.dumps(html_to_shopify_rich_text(str(value)))
    return str(value)


def html_to_shopify_rich_text(html: str) -> dict[str, Any]:
    """
    Convert Wagtail RichTextField HTML into Shopify rich_text_field JSON.
    Shopify expects a structured document, not raw HTML strings.
    """
    html = (html or "").strip()
    if not html:
        return {"type": "root", "children": []}
    if html.startswith("{") and '"type"' in html and '"root"' in html:
        try:
            parsed = json.loads(html)
            if isinstance(parsed, dict) and parsed.get("type") == "root":
                return parsed
        except json.JSONDecodeError:
            pass
    parser = _ShopifyRichTextHTMLParser()
    parser.feed(html)
    parser.close()
    children = parser.blocks
    if not children:
        text = re.sub(r"<[^>]+>", "", html).strip()
        if text:
            children = [_paragraph([_text(text)])]
    return {"type": "root", "children": children}


def _text(value: str, **attrs: Any) -> dict[str, Any]:
    node: dict[str, Any] = {"type": "text", "value": value}
    node.update(attrs)
    return node


def _paragraph(children: list[dict[str, Any]]) -> dict[str, Any]:
    return {"type": "paragraph", "children": children or [_text("")]}


class _ShopifyRichTextHTMLParser(HTMLParser):
    BLOCK_TAGS = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6"}
    HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks: list[dict[str, Any]] = []
        self._block_stack: list[dict[str, Any]] = []
        self._inline_stack: list[dict[str, Any]] = []
        self._list_stack: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr_map = {key: (value or "") for key, value in attrs}
        if tag in self.HEADING_TAGS:
            level = int(tag[1])
            self._block_stack.append({"type": "heading", "level": level, "children": []})
        elif tag in {"ul", "ol"}:
            list_type = "ordered" if tag == "ol" else "unordered"
            node = {"type": "list", "listType": list_type, "children": []}
            self._list_stack.append(node)
            if self._block_stack:
                self._block_stack[-1]["children"].append(node)
            else:
                self.blocks.append(node)
        elif tag == "li":
            item = {"type": "list-item", "children": []}
            if self._list_stack:
                self._list_stack[-1]["children"].append(item)
            self._block_stack.append(item)
        elif tag in {"strong", "b"}:
            self._inline_stack.append({"bold": True})
        elif tag in {"em", "i"}:
            self._inline_stack.append({"italic": True})
        elif tag == "a":
            self._inline_stack.append(
                {
                    "link": {
                        "type": "link",
                        "url": attr_map.get("href", ""),
                        "title": attr_map.get("title") or None,
                        "target": attr_map.get("target") or None,
                        "children": [],
                    }
                }
            )
        elif tag in self.BLOCK_TAGS and tag not in self.HEADING_TAGS:
            self._block_stack.append({"type": "paragraph", "children": []})
        elif tag == "br":
            self._append_inline(_text("\n"))

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.HEADING_TAGS or tag in {"p", "div", "li"}:
            if self._block_stack:
                block = self._block_stack.pop()
                if block["type"] == "list-item":
                    if not block["children"]:
                        block["children"] = [_text("")]
                elif block["type"] == "heading" and not block["children"]:
                    block["children"] = [_text("")]
                elif block["type"] == "paragraph" and not block["children"]:
                    block["children"] = [_text("")]
                if block["type"] == "list-item":
                    return
                if self._block_stack:
                    self._block_stack[-1]["children"].append(block)
                else:
                    self.blocks.append(block)
        elif tag in {"ul", "ol"}:
            if self._list_stack:
                self._list_stack.pop()
        elif tag in {"strong", "b", "em", "i"}:
            if self._inline_stack:
                self._inline_stack.pop()
        elif tag == "a":
            if self._inline_stack and "link" in self._inline_stack[-1]:
                link_node = self._inline_stack.pop()["link"]
                if not link_node["children"]:
                    link_node["children"] = [_text("")]
                self._append_inline(link_node)

    def handle_data(self, data: str) -> None:
        if not data:
            return
        self._append_inline(_text(data, **self._current_inline_attrs()))

    def _current_inline_attrs(self) -> dict[str, Any]:
        attrs: dict[str, Any] = {}
        for frame in self._inline_stack:
            if "link" in frame:
                continue
            attrs.update(frame)
        return attrs

    def _append_inline(self, node: dict[str, Any]) -> None:
        if self._block_stack:
            self._block_stack[-1]["children"].append(node)
        elif self._list_stack:
            current_list = self._list_stack[-1]
            if current_list["children"]:
                current_list["children"][-1]["children"].append(node)
            else:
                item = {"type": "list-item", "children": [node]}
                current_list["children"].append(item)
        else:
            self.blocks.append(_paragraph([node]))


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
