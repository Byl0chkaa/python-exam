import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')
app = Celery('configs', include=['core.services.email_service'])
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-rates-every-day': {
        'task': 'apps.ads.tasks.update_exchange_task',
        'schedule': crontab(hour=6, minute=0),
    },
}
