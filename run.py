from os import environ
from dotenv import load_dotenv
from app import create_app
from app.tasks import update_exchange_rates
from datetime import timedelta

from celery import current_app as celery_app
from redbeat import RedBeatSchedulerEntry
from celery.schedules import crontab

load_dotenv()
dsn = environ.get("SQLALCHEMY_DATABASE_URI")
app, celery = create_app(dsn=dsn)

schedule_name = "update_exchange_rates"
# interval = crontab(hour='1,23', minute=0)
interval = timedelta(seconds=10)
entry = RedBeatSchedulerEntry(schedule_name, "app.tasks.update_exchange_rates", interval, args=[schedule_name], app=celery)
entry.save()
# app.app_context().push()
