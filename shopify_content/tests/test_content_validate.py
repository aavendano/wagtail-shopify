"""content_validate management command (CS4)."""

import json
import tempfile
from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings

from shopify_content.content_store.backends import FilesystemContentRepository
from shopify_content.content_store.contracts import ContentRef
from shopify_content.content_store.serializers import FrontmatterVerbatimSerializer


@override_settings(CONTENT_STORE_ROOT="/tmp/unused")
class ContentValidateCommandTests(TestCase):
    def test_validate_exits_nonzero_on_invalid_frontmatter(self):
        root = tempfile.mkdtemp()
        bad = "---\n: invalid\n---\nbody"
        path = __import__("pathlib").Path(root) / "en-us" / "shopify_content" / "blogpage" / "1" / "description.md"
        path.parent.mkdir(parents=True)
        path.write_text(bad, encoding="utf-8")

        with override_settings(CONTENT_STORE_ROOT=root):
            out = StringIO()
            with self.assertRaises(SystemExit) as ctx:
                call_command("content_validate", "--json", stdout=out)
            self.assertEqual(ctx.exception.code, 1)
            payload = json.loads(out.getvalue())
            self.assertFalse(payload["ok"])

    def test_validate_ok_on_valid_file(self):
        root = tempfile.mkdtemp()
        ref = ContentRef("shopify_content.blogpage", "2", "description", "en-US")
        ser = FrontmatterVerbatimSerializer()
        rel = __import__("pathlib").Path("en-us/shopify_content/blogpage/2/description.md")
        path = __import__("pathlib").Path(root) / rel
        path.parent.mkdir(parents=True)
        path.write_text(ser.dumps(ref, "hello", meta={}), encoding="utf-8")

        with override_settings(CONTENT_STORE_ROOT=root):
            out = StringIO()
            call_command("content_validate", "--json", stdout=out)
            payload = json.loads(out.getvalue())
            self.assertTrue(payload["ok"])
