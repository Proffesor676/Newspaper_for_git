import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newspaper.settings')

app = Celery('newspaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'when_creating_post': {
        'task': 'news.tasks.notify_about_new_post',
        'schedule': 30,
    },
}
app.conf.beat_schedule = {
    'when_week': {
        'task': 'news.tasks.notify_weekly',
        'schedule': 30,
    },
}

