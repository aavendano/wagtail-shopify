import tempfile
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.test import Client, TestCase, override_settings

from admin_theme.wagtail_hooks import CHEESECAKE_ADMIN_CSS


class WhiteNoiseServesCollectedStaticTests(TestCase):
    """Production has DEBUG off: the app itself must serve STATIC_ROOT under /static/."""

    def test_middleware_follows_security_middleware(self):
        middleware = settings.MIDDLEWARE
        self.assertEqual(
            middleware.index('whitenoise.middleware.WhiteNoiseMiddleware'),
            middleware.index('django.middleware.security.SecurityMiddleware') + 1,
        )

    def test_collected_theme_css_and_fonts_are_served_with_debug_off(self):
        with tempfile.TemporaryDirectory() as static_root:
            with override_settings(DEBUG=False, STATIC_ROOT=static_root):
                call_command('collectstatic', interactive=False, verbosity=0)
                font = next(Path(static_root, 'admin_theme', 'fonts').glob('*.woff2'))
                # The middleware indexes STATIC_ROOT when the first request loads it.
                client = Client()

                css = client.get(f'/static/{CHEESECAKE_ADMIN_CSS}')
                self.assertEqual(css.status_code, 200)
                self.assertIn('text/css', css['Content-Type'])
                self.assertIn(b'--w-color-primary-hue', b''.join(css.streaming_content))

                font_response = client.get(f'/static/admin_theme/fonts/{font.name}')
                self.assertEqual(font_response.status_code, 200)
                self.assertEqual(font_response['Content-Type'], 'font/woff2')

    def test_files_not_collected_are_not_served(self):
        with tempfile.TemporaryDirectory() as static_root:
            with override_settings(DEBUG=False, STATIC_ROOT=static_root):
                response = Client().get(f'/static/{CHEESECAKE_ADMIN_CSS}')
                self.assertEqual(response.status_code, 404)
