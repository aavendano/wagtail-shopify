"""Phase E tests: Git-authoritative LocationPage RichText sections."""

import tempfile
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase, override_settings
from wagtail.models import Locale, Page

from shopify_content.content_store.accessors import db_text
from shopify_content.content_store.backends import FilesystemContentRepository
from shopify_content.content_store.contracts import ContentNotFound
from shopify_content.content_store.refs import ref_for, relative_path
from shopify_content.models import LocationPage, ShopifyRootPage
from shopify_content.sync.location_editorial import LOCATION_EDITORIAL_FIELDS


DB_VALUES = {
    'intro': '<p>DB intro</p>',
    'content_2': '<p>DB section 2</p>',
    'content_3': '<p>DB section 3</p>',
    'brand_section_content': '<p>DB brand</p>',
    'map_content': '<p>DB map</p>',
    'after_page_content': '<p>DB closing</p>',
}

GIT_VALUES = {
    field: value.replace('DB', 'GIT')
    for field, value in DB_VALUES.items()
}


def _make_location(**overrides):
    locale, _ = Locale.objects.get_or_create(language_code='en-US')
    home = Page.objects.filter(depth=1).first() or Page.objects.first()
    root = ShopifyRootPage(
        title='Locations', slug=f"locations-{LocationPage.objects.count()}",
        locale=locale, sync_enabled=False,
    )
    home.add_child(instance=root)

    values = {
        'title': 'Austin',
        'titulo': 'Austin',
        'city': 'Austin',
        'state': 'Texas',
        'slug': f"en-us-austin-{LocationPage.objects.count()}",
        'handle': f"en-us-austin-{LocationPage.objects.count()}",
        'locale': locale,
        'sync_enabled': True,
        **DB_VALUES,
    }
    values.update(overrides)
    page = LocationPage(**values)
    root.add_child(instance=page)
    return page


def _write_git(root, page, values=None):
    repo = FilesystemContentRepository(root)
    for field_key, value in (values or GIT_VALUES).items():
        repo.write(ref_for(page, field_key), value)


@override_settings(CONTENT_STORE_MODE='git_authoritative')
class LocationGitAuthorityTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(CONTENT_STORE_ROOT=self.root)
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    def test_registry_contains_all_six_location_richtext_fields(self):
        self.assertEqual(set(LOCATION_EDITORIAL_FIELDS), set(DB_VALUES))

    def test_domain_api_returns_git_for_every_location_richtext_field(self):
        page = _make_location()
        _write_git(self.root, page)

        for field_key, git_value in GIT_VALUES.items():
            self.assertEqual(getattr(page.editorial, field_key), git_value)
            self.assertEqual(db_text(page, field_key), DB_VALUES[field_key])

    def test_missing_authoritative_file_aborts_resolution(self):
        page = _make_location()
        partial = dict(GIT_VALUES)
        partial.pop('map_content')
        _write_git(self.root, page, partial)

        with self.assertRaises(ContentNotFound):
            _ = page.editorial.map_content

    def test_path_is_locale_and_pk_stable(self):
        page = _make_location()
        rel = relative_path(ref_for(page, 'intro')).as_posix()
        self.assertEqual(
            rel,
            f'en-us/shopify_content/locationpage/{page.pk}/intro.md',
        )
        before = rel
        page.slug = 'renamed-location'
        page.save()
        after = relative_path(ref_for(page, 'intro')).as_posix()
        self.assertEqual(before, after)


@override_settings(CONTENT_STORE_MODE='git_authoritative')
class LocationPublicationAdapterTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(CONTENT_STORE_ROOT=self.root)
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    def test_outbound_import_surface_uses_git_values_and_restores_db(self):
        page = _make_location()
        _write_git(self.root, page)
        captured = {}

        def fake_legacy_sync(current):
            for field_key in LOCATION_EDITORIAL_FIELDS:
                captured[field_key] = getattr(current, field_key)
            return True, 'ok'

        with patch(
            'shopify_content.sync.location_editorial._legacy_sync_location_page',
            side_effect=fake_legacy_sync,
        ):
            from shopify_content.sync.outbound import sync_location_page
            ok, message = sync_location_page(page)

        self.assertTrue(ok, message)
        self.assertEqual(captured, GIT_VALUES)
        for field_key, db_value in DB_VALUES.items():
            self.assertEqual(db_text(page, field_key), db_value)

    def test_overlay_restores_db_values_when_legacy_sync_raises(self):
        page = _make_location()
        _write_git(self.root, page)

        with patch(
            'shopify_content.sync.location_editorial._legacy_sync_location_page',
            side_effect=RuntimeError('shopify unavailable'),
        ):
            from shopify_content.sync.outbound import sync_location_page
            with self.assertRaisesRegex(RuntimeError, 'shopify unavailable'):
                sync_location_page(page)

        for field_key, db_value in DB_VALUES.items():
            self.assertEqual(db_text(page, field_key), db_value)

    def test_missing_file_prevents_legacy_sync(self):
        page = _make_location()
        _write_git(self.root, page, {'intro': GIT_VALUES['intro']})

        with patch(
            'shopify_content.sync.location_editorial._legacy_sync_location_page',
        ) as legacy:
            from shopify_content.sync.outbound import sync_location_page
            with self.assertRaises(ContentNotFound):
                sync_location_page(page)
            legacy.assert_not_called()


class LocationMaterializationTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(
            CONTENT_STORE_ROOT=self.root,
            CONTENT_STORE_MODE='git_authoritative',
        )
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    def test_materialize_one_location_field_verbatim(self):
        page = _make_location()
        out = StringIO()
        call_command(
            'materialize_editorial_content',
            field='intro', stdout=out,
        )
        self.assertIn('created=1', out.getvalue())
        value = FilesystemContentRepository(self.root).read(ref_for(page, 'intro')).body
        self.assertEqual(value, DB_VALUES['intro'])


@override_settings(CONTENT_STORE_MODE='mirror')
class LocationMirrorSignalTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(CONTENT_STORE_ROOT=self.root)
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    def test_registry_driven_signal_mirrors_location_fields(self):
        page = _make_location()
        page.intro = '<p>Mirror update</p>'
        with self.captureOnCommitCallbacks(execute=True):
            page.save()

        repo = FilesystemContentRepository(self.root)
        self.assertEqual(
            repo.read(ref_for(page, 'intro')).body,
            '<p>Mirror update</p>',
        )
