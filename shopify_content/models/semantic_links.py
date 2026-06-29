from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable

from shopify_content.semantic_links.constants import (
    LEGACY_SEMANTIC_LINK_MODEL_NAMES,
    PARENT_PAGE_CONFIG,
    RELATION_CONFIG,
    RELATION_TO_TYPE,
    SEMANTIC_LINK_RELATION_NAMES,
    TYPE_TO_RELATION,
)


class SemanticPageLink(Orderable):
    """
    Abstract internal link from a content page to a typed Wagtail Page.

    is_auto=True rows are replaced on semantic refresh; is_auto=False are editor-curated.
    """

    related_page = models.ForeignKey(
        'wagtailcore.Page',
        related_name='+',
        on_delete=models.CASCADE,
    )
    is_auto = models.BooleanField(
        default=False,
        db_default=False,
        help_text='True when created by semantic auto-generation on publish.',
    )

    class Meta(Orderable.Meta):
        abstract = True

    def clean(self):
        super().clean()
        expected_type = getattr(self.__class__, 'expected_type_key', None)
        if expected_type and self.related_page_id:
            from shopify_content.semantic_links.service import page_type_key_for

            actual = page_type_key_for(self.related_page)
            if actual != expected_type:
                raise ValidationError(
                    {
                        'related_page': (
                            f'Expected a {expected_type} page, got {actual or "unknown"}.'
                        ),
                    }
                )


def _page_chooser_panel():
    return FieldPanel('related_page')


def _make_typed_link_model(*, parent_label, parent_model_path, parent_short_name, relation_name):
    config = RELATION_CONFIG[relation_name]
    type_suffix = config['type_suffix']
    class_name = f'{parent_short_name}Related{type_suffix}Link'
    verbose_name = config['label']
    verbose_name_plural = config['heading']

    Meta = type(
        'Meta',
        (Orderable.Meta,),
        {
            'verbose_name': verbose_name,
            'verbose_name_plural': verbose_name_plural,
        },
    )

    return type(
        class_name,
        (SemanticPageLink,),
        {
            'expected_type_key': config['type_key'],
            'page': ParentalKey(
                parent_model_path,
                related_name=relation_name,
                on_delete=models.CASCADE,
            ),
            'panels': [_page_chooser_panel()],
            'Meta': Meta,
            '__module__': __name__,
        },
    )


TYPED_SEMANTIC_LINK_MODELS: dict[tuple[str, str], type] = {}
ALL_TYPED_SEMANTIC_LINK_MODELS: list[type] = []

for parent_label, parent_model_path, parent_short_name in PARENT_PAGE_CONFIG:
    for relation_name in SEMANTIC_LINK_RELATION_NAMES:
        model_cls = _make_typed_link_model(
            parent_label=parent_label,
            parent_model_path=parent_model_path,
            parent_short_name=parent_short_name,
            relation_name=relation_name,
        )
        TYPED_SEMANTIC_LINK_MODELS[(parent_label, relation_name)] = model_cls
        ALL_TYPED_SEMANTIC_LINK_MODELS.append(model_cls)
        globals()[model_cls.__name__] = model_cls


def get_typed_link_model(parent_page, relation_name: str):
    parent_label = type(parent_page).__name__
    return TYPED_SEMANTIC_LINK_MODELS.get((parent_label, relation_name))


def iter_semantic_link_relations(page):
    for relation_name in SEMANTIC_LINK_RELATION_NAMES:
        manager = getattr(page, relation_name, None)
        if manager is not None:
            yield relation_name, manager


def iter_typed_link_models_for_page(page):
    parent_label = type(page).__name__
    for (label, relation_name), model_cls in TYPED_SEMANTIC_LINK_MODELS.items():
        if label == parent_label:
            yield relation_name, model_cls


def count_auto_semantic_links(page) -> int:
    total = 0
    for _relation_name, model_cls in iter_typed_link_models_for_page(page):
        total += model_cls.objects.filter(page_id=page.pk, is_auto=True).count()
    return total


def delete_auto_semantic_links(page) -> int:
    removed = 0
    for _relation_name, model_cls in iter_typed_link_models_for_page(page):
        qs = model_cls.objects.filter(page_id=page.pk, is_auto=True)
        removed += qs.count()
        qs.delete()
    return removed


def manual_related_page_pks(page) -> set[int]:
    pks: set[int] = set()
    for _relation_name, model_cls in iter_typed_link_models_for_page(page):
        pks.update(
            model_cls.objects.filter(page_id=page.pk, is_auto=False).values_list(
                'related_page_id',
                flat=True,
            )
        )
    return pks


def all_related_page_pks(page) -> set[int]:
    pks: set[int] = set()
    for _relation_name, model_cls in iter_typed_link_models_for_page(page):
        pks.update(
            model_cls.objects.filter(page_id=page.pk).values_list(
                'related_page_id',
                flat=True,
            )
        )
    return pks


def page_has_semantic_links(page) -> bool:
    for _relation_name, model_cls in iter_typed_link_models_for_page(page):
        if model_cls.objects.filter(page_id=page.pk).exists():
            return True
    return False


def page_has_auto_semantic_links(page) -> bool:
    return count_auto_semantic_links(page) > 0


def relation_for_page_type(type_key: str) -> str:
    return TYPE_TO_RELATION[type_key]


def type_key_for_relation(relation_name: str) -> str:
    return RELATION_TO_TYPE[relation_name]
