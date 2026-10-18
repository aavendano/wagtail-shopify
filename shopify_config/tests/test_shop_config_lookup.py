from django.test import TestCase

from shopify_config.models import ShopConfig
from shopify_config.shop_config_lookup import get_shop_config, shop_has_access_token


class ShopConfigLookupTests(TestCase):
    def test_prefers_record_with_token_when_multiple_shop_formats_exist(self):
        ShopConfig.objects.create(shop="demo", is_online=False, access_token=None)
        ShopConfig.objects.create(
            shop="demo.myshopify.com", is_online=False, access_token="tok"
        )

        self.assertTrue(shop_has_access_token("demo.myshopify.com"))
        self.assertEqual(get_shop_config("demo").access_token, "tok")

    def test_get_shop_config_without_shop_prefers_row_with_token(self):
        ShopConfig.objects.create(shop="empty-shop", is_online=False, access_token=None)
        ShopConfig.objects.create(
            shop="ready-shop", is_online=False, access_token="tok"
        )

        config = get_shop_config()
        self.assertEqual(config.shop, "ready-shop")
        self.assertTrue(shop_has_access_token())
