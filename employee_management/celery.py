from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','employee_management.settings')

app = Celery('employee_management')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings,namespace='CELERY')


#celery beat settings

app.autodiscover_tasks()

