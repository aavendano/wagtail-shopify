from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.test import TestCase


class PlayLoveToysBrandingTests(TestCase):
    def test_login_page_is_branded(self):
        response = self.client.get('/admin/login/')
        self.assertContains(response, 'Sign in to PlayLoveToys')
        self.assertContains(response, 'plt-logo-on-light.svg')
        self.assertContains(response, 'plt-logo.svg')
        self.assertContains(response, 'favicon-32x32.png')
        self.assertContains(response, '- PlayLoveToys</title>')
        self.assertContains(response, 'admin_theme/css/branding.css')
        self.assertNotContains(response, 'Sign in to Wagtail')

    def test_sidebar_uses_playlovetoys_logo(self):
        user = get_user_model().objects.create_superuser('branding', 'b@example.com', 'pw-branding-123')
        self.client.force_login(user)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-wagtail-sidebar-branding-logo')
        self.assertContains(response, 'class="plt-admin-logo"')
        self.assertContains(response, 'alt="PlayLoveToys"')

    def test_branding_assets_are_served(self):
        for path in (
            'admin_theme/img/plt-logo.svg',
            'admin_theme/img/plt-logo-on-light.svg',
            'admin_theme/img/favicon-32x32.png',
            'admin_theme/css/branding.css',
        ):
            self.assertIsNotNone(finders.find(path), path)

    def test_light_logo_has_no_white_fills(self):
        svg = open(finders.find('admin_theme/img/plt-logo-on-light.svg')).read().lower()
        for white in ('#fefefe', '#fdfdfd', '#f6f6f6'):
            self.assertNotIn(white, svg)
