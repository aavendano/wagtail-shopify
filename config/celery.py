import os

from config.bigframes_bootstrap import ensure_bigframes_pre_django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
ensure_bigframes_pre_django()

from celery import Celery

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
