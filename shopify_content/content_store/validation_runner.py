"""Deterministic validation of the deployed editorial content tree."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from shopify_content.content_store.backends import FilesystemContentRepository
from shopify_content.content_store.contracts import (
    ContentNotFound,
    InvalidEditorialFrontmatter,
)
from shopify_content.content_store.markdown.errors import MarkdownRenderError
from shopify_content.content_store.markdown.renderer import render_editorial_markdown
from shopify_content.content_store.markdown.validation import validate_directive_structure
from shopify_content.content_store.serializers import split_frontmatter


@dataclass
class ValidationIssue:
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


@dataclass
class ValidationReport:
    ok: bool
    checked: int = 0
    issues: list[ValidationIssue] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "checked": self.checked,
            "issues": [i.as_dict() for i in self.issues],
        }

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), indent=2, sort_keys=True)


def validate_content_tree(root: str | Path) -> ValidationReport:
    root_path = Path(root)
    report = ValidationReport(ok=True)
    if not root_path.is_dir():
        report.ok = False
        report.issues.append(
            ValidationIssue("missing_root", str(root_path), "Content root does not exist.")
        )
        return report

    repo = FilesystemContentRepository(root_path)

    for path in sorted(root_path.rglob("*.md")):
        rel = path.relative_to(root_path).as_posix()
        report.checked += 1
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError as exc:
            report.ok = False
            report.issues.append(ValidationIssue("read_error", rel, str(exc)))
            continue

        try:
            split_frontmatter(raw)
        except InvalidEditorialFrontmatter as exc:
            report.ok = False
            report.issues.append(ValidationIssue("invalid_frontmatter", rel, str(exc)))
            continue

        # Resolve ref when path matches canonical layout.
        parts = path.relative_to(root_path).parts
        if len(parts) >= 5:
            from shopify_content.content_store.content_index_service import _ref_from_relative

            ref = _ref_from_relative(path.relative_to(root_path))
            if ref is not None:
                try:
                    doc = repo.read_canonical(ref)
                    if doc.checksum != doc.as_content_document().checksum:
                        report.ok = False
                        report.issues.append(
                            ValidationIssue("checksum_mismatch", rel, "Checksum inconsistent.")
                        )
                    if ref.field_key == "body" and ref.content_type.endswith("articlepage"):
                        validate_directive_structure(doc.body)
                        render_editorial_markdown(doc.body)
                except ContentNotFound as exc:
                    report.ok = False
                    report.issues.append(ValidationIssue("not_found", rel, str(exc)))
                except MarkdownRenderError as exc:
                    report.ok = False
                    report.issues.append(ValidationIssue("render_error", rel, str(exc)))

    return report
