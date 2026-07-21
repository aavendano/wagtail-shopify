"""
Workaround for django-ai-core 0.1.5 ModelSource.post_index_update.

Upstream passes the VectorIndex *instance* as index_name. Django stores
``str(index)``, which includes a process-local memory address
(``<PageIndex object at 0x...>``). Each update therefore creates a new
unique key and never deletes the previous rows, causing unbounded growth
in ``index_modelsourceindex``.

This patch:
- uses the stable registry name (``index.__class__.__name__``, e.g. PageIndex)
- syncs only stable-name rows (insert missing / delete obsolete)
- leaves historical broken ``object at 0x...`` rows untouched for later cleanup
"""

from __future__ import annotations

import logging

from django.db import IntegrityError, transaction

logger = logging.getLogger(__name__)

_PATCH_ATTR = '_shopify_stable_index_name_patched'


def stable_index_name(index) -> str:
    """Return the canonical index name used by django-ai-core IndexRegistry."""
    if isinstance(index, str):
        return index
    return index.__class__.__name__


def patched_post_index_update(self, index) -> None:
    """Idempotent sync of ModelSourceIndex using a stable index_name."""
    from django.contrib.contenttypes.models import ContentType
    from django_ai_core.contrib.index.models import ModelSourceIndex

    index_name = stable_index_name(index)
    source_id = self.source_id
    content_type = ContentType.objects.get_for_model(self.model)

    desired_ids = {
        int(pk)
        for pk in self.queryset.values_list('pk', flat=True)
    }

    existing_ids = set(
        ModelSourceIndex.objects.filter(
            content_type=content_type,
            index_name=index_name,
            source_id=source_id,
        ).values_list('object_id', flat=True)
    )

    to_add = desired_ids - existing_ids
    to_remove = existing_ids - desired_ids

    if to_add:
        rows = [
            ModelSourceIndex(
                content_type=content_type,
                object_id=object_id,
                index_name=index_name,
                source_id=source_id,
            )
            for object_id in to_add
        ]
        try:
            with transaction.atomic():
                ModelSourceIndex.objects.bulk_create(rows, ignore_conflicts=True)
        except TypeError:
            # Django < 2.2 fallback (should not happen on this stack)
            for object_id in to_add:
                try:
                    with transaction.atomic():
                        ModelSourceIndex.objects.get_or_create(
                            content_type=content_type,
                            object_id=object_id,
                            index_name=index_name,
                            source_id=source_id,
                        )
                except IntegrityError:
                    pass

    if to_remove:
        ModelSourceIndex.objects.filter(
            content_type=content_type,
            index_name=index_name,
            source_id=source_id,
            object_id__in=to_remove,
        ).delete()


def install_stable_index_name_fix() -> bool:
    """Monkey-patch ModelSource.post_index_update. Idempotent."""
    try:
        from django_ai_core.contrib.index.source import ModelSource
    except ImportError:
        logger.debug('django_ai_core not installed; skipping index tracking fix')
        return False

    if getattr(ModelSource.post_index_update, _PATCH_ATTR, False):
        return False

    ModelSource.post_index_update = patched_post_index_update
    setattr(ModelSource.post_index_update, _PATCH_ATTR, True)
    logger.info(
        'Installed django-ai-core ModelSource.post_index_update stable index_name fix'
    )
    return True
