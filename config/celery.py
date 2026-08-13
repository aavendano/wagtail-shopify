import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# BigFrames must load before Django/zope.interface when this process runs GSC tasks.
# Shopify-only workers omit CMS_SHOP_LOAD_BIGFRAMES to keep the baseline lean.
_load_bigframes = os.environ.get('CMS_SHOP_LOAD_BIGFRAMES', '').strip().lower()
if _load_bigframes in ('1', 'true', 'yes'):
    from config.bigframes_bootstrap import ensure_bigframes_pre_django

    ensure_bigframes_pre_django()

from celery import Celery

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
