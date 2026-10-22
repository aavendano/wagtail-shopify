import importlib.util
import shutil
import tempfile
from pathlib import Path

from django.test import SimpleTestCase

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).resolve().parent / 'fixtures'

spec = importlib.util.spec_from_file_location('build_admin_theme', ROOT / 'scripts' / 'build_admin_theme.py')
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


class GeneratorTests(SimpleTestCase):
    def test_renders_brand_surface_and_status_variables(self):
        colors, font = generator.read_tokens(FIXTURE)
        css, checks = generator.render(colors, font, 'abc123')

        self.assertIn('@ abc123', css)
        self.assertIn('--w-font-sans: "Atkinson Hyperlegible", Arial, sans-serif;', css)
        self.assertIn('--w-color-surface-page: #FAF7F2;', css)
        for family in ('info-125', 'positive-100', 'warning-100', 'critical-200'):
            self.assertIn(f'--w-color-{family}-hue', css)
        self.assertTrue(checks)

    def test_output_is_deterministic(self):
        colors, font = generator.read_tokens(FIXTURE)
        self.assertEqual(generator.render(colors, font, 'x'), generator.render(colors, font, 'x'))

    def test_every_check_meets_aa(self):
        colors, font = generator.read_tokens(FIXTURE)
        _, checks = generator.render(colors, font, 'x')
        for line in checks:
            self.assertGreaterEqual(float(line.rsplit(': ', 1)[1].split(':')[0]), generator.AA_TEXT, line)

    def test_low_contrast_tokens_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(FIXTURE, tmp, dirs_exist_ok=True)
            colors_css = Path(tmp) / 'packages/design-system/src/tokens/colors.css'
            text = colors_css.read_text().replace(
                '--plt-color-base-content: oklch(37% 0.044 257.287);',
                '--plt-color-base-content: oklch(85% 0.02 257);',
            )
            colors_css.write_text(text)
            colors, font = generator.read_tokens(Path(tmp))
            with self.assertRaises(SystemExit):
                generator.render(colors, font, 'x')

    def test_missing_tokens_fail_loudly(self):
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(FIXTURE, tmp, dirs_exist_ok=True)
            colors_css = Path(tmp) / 'packages/design-system/src/tokens/colors.css'
            colors_css.write_text(':root { --plt-color-primary: #533278; }')
            colors, font = generator.read_tokens(Path(tmp))
            with self.assertRaises(SystemExit):
                generator.render(colors, font, 'x')
