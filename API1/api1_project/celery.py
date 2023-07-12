import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api1_project.settings')
app = Celery('ap1')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Beat Settings
app.autodiscover_tasks()

app.conf.beat_scheduler = 'django_celery_beat.scheduler.DatabaseScheduler'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
