from django.db import models


class ContentUrlIndex(models.Model):
    """
    Materialized mapping from Shopify storefront URL paths to Wagtail pages.

    Used to correlate GSC traffic URLs with CMS content. Rebuilt on publish
    and via rebuild_content_url_index management command.
    """

    normalized_path = models.CharField(
        max_length=500,
        db_index=True,
        help_text='Storefront path without domain or locale prefix, e.g. /pages/glossary/alpha',
    )
    wagtail_page = models.ForeignKey(
        'wagtailcore.Page',
        on_delete=models.CASCADE,
        related_name='content_url_index_entries',
    )
    content_type = models.CharField(
        max_length=32,
        db_index=True,
        help_text='product, collection, blog, article, glossary_term, location, home, index, root',
    )
    handle = models.CharField(max_length=255, blank=True, db_index=True)
    blog_handle = models.CharField(
        max_length=255,
        blank=True,
        help_text='Parent blog handle for article pages only.',
    )
    locale = models.CharField(
        max_length=16,
        blank=True,
        help_text='Wagtail locale code, e.g. en-US',
    )
    locale_prefix = models.CharField(
        max_length=16,
        blank=True,
        help_text='Shopify Markets URL prefix without slashes, e.g. es-us. Empty for canonical.',
    )
    is_canonical = models.BooleanField(
        default=True,
        help_text='True when normalized_path has no Markets locale prefix variant.',
    )

    class Meta:
        verbose_name = 'Content URL index entry'
        verbose_name_plural = 'Content URL index entries'
        constraints = [
            models.UniqueConstraint(
                fields=['normalized_path', 'locale_prefix'],
                name='uniq_content_url_index_path_prefix',
            ),
        ]
        indexes = [
            models.Index(
                fields=['content_type', 'handle'],
                name='content_url_type_handle_idx',
            ),
            models.Index(
                fields=['content_type', 'blog_handle', 'handle'],
                name='content_url_article_idx',
            ),
        ]

    def __str__(self) -> str:
        prefix = f'/{self.locale_prefix}' if self.locale_prefix else ''
        return f'{prefix}{self.normalized_path} → page {self.wagtail_page_id}'
