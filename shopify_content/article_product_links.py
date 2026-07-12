"""Rewrite /products/{handle} hrefs in article StreamField HTML to live ProductPage handles."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable
from urllib.parse import unquote

from shopify_content.storefront_urls import product_path

# href="..." or href='...' capturing full URL and product handle segment.
PRODUCT_HREF_RE = re.compile(
    r"""href\s*=\s*(?P<q>["'])(?P<url>[^"']*?/products/(?P<handle>[^"'/?#]+))(?P=q)""",
    re.IGNORECASE,
)

# Anchor tags whose href targets /products/...
PRODUCT_ANCHOR_RE = re.compile(
    r"""<a\b([^>]*?\bhref\s*=\s*(?P<q>["'])(?P<url>[^"']*?/products/(?P<handle>[^"'/?#]+))(?P=q)[^>]*)>(?P<body>.*?)</a>""",
    re.IGNORECASE | re.DOTALL,
)

STREAM_HTML_BLOCK_TYPES = frozenset({'html'})
STREAM_RICHTEXT_BLOCK_TYPES = frozenset({'paragraph', 'callout'})

# Trailing color/finish tokens often present in legacy handles but not in current ones.
_VARIANT_SUFFIXES = frozenset({
    'black', 'white', 'pink', 'purple', 'coral', 'aqua', 'teal', 'fuchsia',
    'rose', 'red', 'blue', 'green', 'sage', 'obsidian', 'disco', 'roses',
    'ice', 'grey', 'gray', 'gold', 'silver',
})

_STOP_TOKENS = frozenset({'the', 'and', 'or', 'a', 'an', 'for', 'with', 'by', 'of'})


class LinkAction(str, Enum):
    UNCHANGED = 'unchanged'
    REWRITE = 'rewrite'
    UNWRAP = 'unwrap'
    AMBIGUOUS = 'ambiguous'


@dataclass
class LinkDecision:
    original_handle: str
    action: LinkAction
    resolved_handle: str | None = None
    candidates: tuple[str, ...] = ()


@dataclass
class RewriteStats:
    rewritten: int = 0
    unwrapped: int = 0
    unchanged: int = 0
    ambiguous: int = 0
    decisions: list[LinkDecision] = field(default_factory=list)

    def merge(self, other: RewriteStats) -> None:
        self.rewritten += other.rewritten
        self.unwrapped += other.unwrapped
        self.unchanged += other.unchanged
        self.ambiguous += other.ambiguous
        self.decisions.extend(other.decisions)


def normalize_product_handle(raw: str) -> str:
    """Decode percent-encoding and normalize to a Shopify-style handle."""
    handle = unquote(raw or '').strip()
    handle = handle.lower()
    # Normalize fancy trademark / punctuation leftovers from URLs.
    handle = handle.replace('™', '').replace('®', '').replace('©', '')
    handle = re.sub(r'[_\s]+', '-', handle)
    handle = re.sub(r'-{2,}', '-', handle).strip('-')
    return handle


def extract_product_handles(html: str) -> list[str]:
    """Return normalized handles from product hrefs in HTML (order preserved, deduped)."""
    seen: set[str] = set()
    out: list[str] = []
    for match in PRODUCT_HREF_RE.finditer(html or ''):
        handle = normalize_product_handle(match.group('handle'))
        if handle and handle not in seen:
            seen.add(handle)
            out.append(handle)
    return out


def canonical_product_href(handle: str) -> str:
    return product_path(handle)


class ProductHandleResolver:
    """Resolve legacy product handles to live ProductPage handles."""

    def __init__(
        self,
        live_handles: Iterable[str],
        *,
        shopify_id_to_handle: dict[str, str] | None = None,
        manual_map: dict[str, str] | None = None,
    ):
        self.live_handles = {normalize_product_handle(h) for h in live_handles if h}
        self._live_list = sorted(self.live_handles)
        self.shopify_id_to_handle = {
            str(k): normalize_product_handle(v)
            for k, v in (shopify_id_to_handle or {}).items()
            if v
        }
        self.manual_map = {
            normalize_product_handle(k): normalize_product_handle(v)
            for k, v in (manual_map or {}).items()
            if k and v
        }

    @classmethod
    def from_queryset(cls, queryset, *, manual_map: dict[str, str] | None = None):
        handles: list[str] = []
        id_map: dict[str, str] = {}
        for handle, shopify_id in queryset.values_list('handle', 'shopify_id'):
            if not handle:
                continue
            norm = normalize_product_handle(handle)
            handles.append(norm)
            if shopify_id:
                # gid://shopify/Product/123 → 123
                numeric = str(shopify_id).rsplit('/', 1)[-1]
                if numeric.isdigit():
                    id_map[numeric] = norm
                id_map[str(shopify_id)] = norm
        return cls(handles, shopify_id_to_handle=id_map, manual_map=manual_map)

    def resolve(self, raw_handle: str) -> LinkDecision:
        handle = normalize_product_handle(raw_handle)
        if not handle:
            return LinkDecision(original_handle=raw_handle, action=LinkAction.UNCHANGED)

        if handle in self.manual_map:
            target = self.manual_map[handle]
            if target in self.live_handles:
                action = LinkAction.UNCHANGED if target == handle else LinkAction.REWRITE
                return LinkDecision(
                    original_handle=handle,
                    action=action,
                    resolved_handle=target,
                )
            return LinkDecision(original_handle=handle, action=LinkAction.UNWRAP)

        if handle in self.live_handles:
            return LinkDecision(
                original_handle=handle,
                action=LinkAction.UNCHANGED,
                resolved_handle=handle,
            )

        if handle.isdigit() and handle in self.shopify_id_to_handle:
            target = self.shopify_id_to_handle[handle]
            return LinkDecision(
                original_handle=handle,
                action=LinkAction.REWRITE,
                resolved_handle=target,
            )

        fuzzy = self._fuzzy_unique(handle)
        if len(fuzzy) == 1:
            return LinkDecision(
                original_handle=handle,
                action=LinkAction.REWRITE,
                resolved_handle=fuzzy[0],
            )
        if len(fuzzy) > 1:
            return LinkDecision(
                original_handle=handle,
                action=LinkAction.AMBIGUOUS,
                candidates=tuple(fuzzy),
            )
        return LinkDecision(original_handle=handle, action=LinkAction.UNWRAP)

    def _fuzzy_unique(self, handle: str) -> list[str]:
        candidates: set[str] = set()

        # Prefix / extension: dead is prefix of live (lelo-f2s → lelo-f2s-adaptive-...)
        for live in self._live_list:
            if live.startswith(handle + '-') or handle.startswith(live + '-'):
                candidates.add(live)

        # Strip color suffix and retry prefix match.
        base = self._strip_variant(handle)
        if base != handle:
            for live in self._live_list:
                if live.startswith(base + '-') or live == base or base in live.split('-'):
                    # Prefer lives that contain the full base as contiguous tokens
                    if _handle_contains_tokens(live, base.split('-')):
                        candidates.add(live)

        # Contiguous token containment (all significant tokens of dead in live).
        tokens = [t for t in handle.split('-') if t and t not in _STOP_TOKENS]
        if len(tokens) >= 2:
            token_hits = [
                live for live in self._live_list
                if _handle_contains_tokens(live, tokens)
            ]
            if len(token_hits) == 1:
                return token_hits
            if not candidates and token_hits:
                # Try without trailing variant token
                if tokens[-1] in _VARIANT_SUFFIXES:
                    reduced = tokens[:-1]
                    reduced_hits = [
                        live for live in self._live_list
                        if _handle_contains_tokens(live, reduced)
                    ]
                    if len(reduced_hits) == 1:
                        return reduced_hits

        if len(candidates) == 1:
            return list(candidates)

        # If prefix candidates empty but base token match unique:
        if base != handle:
            base_tokens = [t for t in base.split('-') if t and t not in _STOP_TOKENS]
            if len(base_tokens) >= 2:
                hits = [
                    live for live in self._live_list
                    if _handle_contains_tokens(live, base_tokens)
                ]
                if len(hits) == 1:
                    return hits
                if len(hits) > 1 and not candidates:
                    return hits[:12]  # ambiguous

        if len(candidates) > 1:
            return sorted(candidates)[:12]
        return sorted(candidates)

    @staticmethod
    def _strip_variant(handle: str) -> str:
        parts = handle.split('-')
        while parts and parts[-1] in _VARIANT_SUFFIXES:
            parts.pop()
        return '-'.join(parts) if parts else handle


def _handle_contains_tokens(live: str, tokens: list[str]) -> bool:
    live_parts = live.split('-')
    if not tokens:
        return False
    # Sliding window: tokens appear contiguously in live
    n = len(tokens)
    for i in range(len(live_parts) - n + 1):
        if live_parts[i : i + n] == tokens:
            return True
    # Fallback: all tokens present (non-contiguous) for longer brands
    if n >= 3 and all(t in live_parts for t in tokens):
        return True
    return False


def rewrite_html_product_links(
    html: str,
    resolver: ProductHandleResolver,
    *,
    unwrap_missing: bool = True,
) -> tuple[str, RewriteStats]:
    """
    Rewrite product anchors in HTML.

    - Live/resolved → href=/products/{live_handle} (relative)
    - Ambiguous → leave unchanged
    - Unmapped → unwrap <a> (keep inner HTML) when unwrap_missing
    """
    stats = RewriteStats()
    if not html:
        return html, stats

    def replace_anchor(match: re.Match) -> str:
        raw_handle = match.group('handle')
        decision = resolver.resolve(raw_handle)
        stats.decisions.append(decision)

        if decision.action == LinkAction.UNCHANGED:
            # Normalize absolute / locale-prefixed URLs to canonical relative
            # even when the handle is already live.
            current_url = match.group('url')
            target = canonical_product_href(
                decision.resolved_handle or normalize_product_handle(raw_handle)
            )
            if current_url == target:
                stats.unchanged += 1
                return match.group(0)
            stats.rewritten += 1
            return _rebuild_anchor(match, target)

        if decision.action == LinkAction.REWRITE and decision.resolved_handle:
            stats.rewritten += 1
            return _rebuild_anchor(match, canonical_product_href(decision.resolved_handle))

        if decision.action == LinkAction.AMBIGUOUS:
            stats.ambiguous += 1
            return match.group(0)

        # UNWRAP
        if unwrap_missing:
            stats.unwrapped += 1
            return match.group('body')
        stats.unchanged += 1
        return match.group(0)

    new_html = PRODUCT_ANCHOR_RE.sub(replace_anchor, html)
    return new_html, stats


def _rebuild_anchor(match: re.Match, new_href: str) -> str:
    attrs = match.group(1)
    quote = match.group('q')
    body = match.group('body')
    new_attrs = re.sub(
        r"""href\s*=\s*(["'])([^"']*)\1""",
        f'href={quote}{new_href}{quote}',
        attrs,
        count=1,
        flags=re.I,
    )
    return f'<a{new_attrs}>{body}</a>'


def rewrite_streamfield_raw(
    raw_blocks: list[dict[str, Any]] | None,
    resolver: ProductHandleResolver,
    *,
    unwrap_missing: bool = True,
) -> tuple[list[dict[str, Any]], RewriteStats, bool]:
    """
    Rewrite product links inside StreamField raw_data.

    Returns (new_raw_blocks, stats, changed).
    """
    stats = RewriteStats()
    if not raw_blocks:
        return [], stats, False

    changed = False
    out: list[dict[str, Any]] = []

    for block in raw_blocks:
        block_type = block.get('type')
        value = block.get('value')
        new_block = dict(block)

        if block_type in STREAM_HTML_BLOCK_TYPES and isinstance(value, str):
            new_html, block_stats = rewrite_html_product_links(
                value, resolver, unwrap_missing=unwrap_missing,
            )
            stats.merge(block_stats)
            if new_html != value:
                changed = True
                new_block['value'] = new_html
        elif block_type in STREAM_RICHTEXT_BLOCK_TYPES and isinstance(value, dict):
            text = value.get('text')
            if isinstance(text, str) and text:
                new_text, block_stats = rewrite_html_product_links(
                    text, resolver, unwrap_missing=unwrap_missing,
                )
                stats.merge(block_stats)
                if new_text != text:
                    changed = True
                    new_value = dict(value)
                    new_value['text'] = new_text
                    new_block['value'] = new_value
        out.append(new_block)

    return out, stats, changed


def load_manual_map(path: str | None) -> dict[str, str]:
    if not path:
        return {}
    with open(path, encoding='utf-8') as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError(f'map file must be a JSON object: {path}')
    return {str(k): str(v) for k, v in data.items()}
