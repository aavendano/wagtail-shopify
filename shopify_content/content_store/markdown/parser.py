"""Inspectable Markdown structure via markdown-it-py (no HTML emission here)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from markdown_it import MarkdownIt
from markdown_it.token import Token


@dataclass(frozen=True)
class MarkdownBlock:
    """Lightweight view of a top-level block for validation/indexing."""

    type: str
    tag: str
    map: tuple[int, int] | None
    content: str


def _md() -> MarkdownIt:
    return MarkdownIt("commonmark", {"html": True}).enable("table")


def tokenize(source: str) -> list[Token]:
    return _md().parse(source or "")


def top_level_blocks(source: str) -> list[MarkdownBlock]:
    tokens = tokenize(source)
    lines = (source or "").splitlines()
    blocks: list[MarkdownBlock] = []
    for tok in tokens:
        if tok.nesting != 0:
            continue
        if tok.type.endswith("_open") or tok.type in {"fence", "code_block", "html_block"}:
            content = ""
            if tok.map:
                start, end = tok.map
                content = "\n".join(lines[start:end])
            blocks.append(
                MarkdownBlock(
                    type=tok.type,
                    tag=tok.tag or "",
                    map=tuple(tok.map) if tok.map else None,
                    content=content,
                )
            )
    return blocks


def directive_lines(source: str) -> Iterable[tuple[int, str]]:
    """Yield (line_index, stripped_line) for lines that look like directives."""
    for i, line in enumerate((source or "").splitlines()):
        stripped = line.strip()
        if stripped.startswith("{%"):
            yield i, stripped
