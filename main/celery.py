import os
from celery.schedules import crontab
from celery import Celery
from django.conf  import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


