"""Filesystem ContentRepository with atomic writes.

Knows nothing about Django models — it operates purely on ``ContentRef`` and
serialized text. The DB row remains authoritative in Phase B; this file is a
mirror.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Mapping, Optional

from .contracts import (
    ContentConflict,
    ContentDocument,
    ContentNotFound,
    ContentRef,
)
from .refs import relative_path
from .serializers import FrontmatterVerbatimSerializer, checksum


class FilesystemContentRepository:
    """Stores each editorial payload as one file under ``root``."""

    def __init__(self, root: os.PathLike | str, serializer=None):
        self.root = Path(root).resolve()
        self.serializer = serializer or FrontmatterVerbatimSerializer()

    def _abs(self, ref: ContentRef) -> Path:
        rel = relative_path(ref)
        target = (self.root / rel).resolve()
        # Defense in depth: the resolved path must stay under root.
        if os.path.commonpath([self.root, target]) != str(self.root):
            raise ValueError(f"Refusing path outside content root: {target}")
        return target

    def exists(self, ref: ContentRef) -> bool:
        return self._abs(ref).is_file()

    def read(self, ref: ContentRef) -> ContentDocument:
        path = self._abs(ref)
        try:
            raw = path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise ContentNotFound(str(ref)) from exc
        return self.serializer.loads(ref, raw)

    def write(
        self,
        ref: ContentRef,
        value: str,
        *,
        meta: Optional[Mapping[str, str]] = None,
        expected_version: Optional[str] = None,
    ) -> ContentDocument:
        if expected_version is not None:
            current = self.read(ref).checksum if self.exists(ref) else None
            if current != expected_version:
                raise ContentConflict(
                    f"expected_version={expected_version!r} but stored={current!r}"
                )
        value = value or ""
        text = self.serializer.dumps(ref, value, meta=meta or {})
        path = self._abs(ref)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._atomic_write(path, text)
        return ContentDocument(
            body=value,
            fmt=self.serializer.fmt,
            meta=dict(meta or {}),
            checksum=checksum(value),
        )

    def delete(self, ref: ContentRef) -> None:
        try:
            self._abs(ref).unlink()
        except FileNotFoundError:
            pass

    @staticmethod
    def _atomic_write(path: Path, text: str) -> None:
        """Write to a temp file in the same dir, then os.replace (atomic)."""
        fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", suffix=path.suffix)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(text)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, path)
        except BaseException:
            try:
                os.unlink(tmp)
            except FileNotFoundError:
                pass
            raise
