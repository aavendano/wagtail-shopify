import re
from pathlib import Path

from django.contrib.staticfiles import finders
from django.test import SimpleTestCase, TestCase
from wagtail import hooks

from admin_theme.wagtail_hooks import CHEESECAKE_ADMIN_CSS

APP_DIR = Path(__file__).resolve().parent.parent


class CheesecakeAdminThemeTests(SimpleTestCase):
    def _css(self):
        path = finders.find(CHEESECAKE_ADMIN_CSS)
        self.assertIsNotNone(path, 'cheesecake-admin.css is not served by staticfiles')
        return Path(path).read_text()

    def test_hook_links_stylesheet(self):
        output = ''.join(str(fn()) for fn in hooks.get_hooks('insert_global_admin_css'))
        self.assertIn('<link rel="stylesheet"', output)
        self.assertIn(CHEESECAKE_ADMIN_CSS, output)

    def test_overrides_wagtail_brand_variables(self):
        css = self._css()
        for variable in (
            '--w-color-primary-hue',
            '--w-color-secondary-hue',
            '--w-color-surface-page: #FAF7F2',
            '--w-font-sans',
        ):
            self.assertIn(variable, css)
        self.assertIn('Atkinson Hyperlegible', css)

    def test_dark_theme_is_left_to_wagtail(self):
        rules = re.sub(r'/\*.*?\*/', '', self._css(), flags=re.S)
        self.assertNotIn('.w-theme-dark', rules)

    def test_fonts_referenced_by_css_exist(self):
        css = self._css()
        referenced = set(re.findall(r'\.\./fonts/([\w.-]+\.woff2)', css))
        self.assertTrue(referenced)
        for name in referenced:
            self.assertIsNotNone(finders.find(f'admin_theme/fonts/{name}'), name)

    def test_header_sha_matches_pinned_sha(self):
        pinned = (APP_DIR / 'DESIGN_SYSTEM_SHA').read_text().strip()
        self.assertIn(f'@ {pinned}', self._css())


class CheesecakeAdminLoginTests(TestCase):
    def test_login_page_includes_theme(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin_theme/css/cheesecake-admin.css')
