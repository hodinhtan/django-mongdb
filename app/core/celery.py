from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(self.request)


app.conf.beat_schedule = {
    # "run-me-every-ten-seconds": {"task": "notifications.task.check", "schedule": 10.0},
    "run-me-every-day": {
        "task": "notifications.task.send_daily_report",
        "schedule": crontab(minute=0, hour=0),
    },
}
