"""Derived index for Git-authoritative editorial content (rebuildable)."""

from django.db import models


class ContentIndex(models.Model):
    """One row per ``ContentRef`` discovered in the deployed content tree."""

    content_type = models.CharField(max_length=128, db_index=True)
    object_id = models.CharField(max_length=64, db_index=True)
    field_key = models.CharField(max_length=64, db_index=True)
    locale = models.CharField(max_length=16, db_index=True)
    checksum = models.CharField(max_length=64, blank=True)
    reference_count = models.PositiveIntegerField(default=0)
    relative_path = models.CharField(max_length=512, blank=True)
    indexed_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["content_type", "object_id", "field_key", "locale"],
                name="uniq_content_index_ref",
            ),
        ]


class ContentReferenceIndex(models.Model):
    """Typed references extracted from a indexed document body."""

    content_index = models.ForeignKey(
        ContentIndex,
        on_delete=models.CASCADE,
        related_name="references",
    )
    ref_type = models.CharField(max_length=32, db_index=True)
    identifier = models.CharField(max_length=255, db_index=True)
    token = models.CharField(max_length=512)

    class Meta:
        indexes = [
            models.Index(fields=["ref_type", "identifier"], name="content_ref_type_ident_idx"),
        ]
