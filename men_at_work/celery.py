import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'men_at_work.settings')

app = Celery('men_at_work')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
