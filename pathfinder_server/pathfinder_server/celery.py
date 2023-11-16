from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'pathfinder_server.settings.common' # need to change to prod.py when deploy
)

app = Celery('pathfinder_server')

app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
)

app.autodiscover_tasks()