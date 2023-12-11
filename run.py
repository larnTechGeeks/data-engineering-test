from os import environ
from dotenv import load_dotenv
from app import create_app
from datetime import timedelta

from celery import current_app as celery_app
from redbeat import RedBeatSchedulerEntry
from celery.schedules import crontab
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from app.tasks import update_exchange_rates_scheduler

load_dotenv()
dsn = environ.get("SQLALCHEMY_DATABASE_URI")
app, celery = create_app(dsn=dsn)

app.app_context().push()

# Scheduling using Celery
schedule_name = "update_exchange_rates"
interval = crontab(hour='1,23', minute=0)
entry = RedBeatSchedulerEntry(schedule_name, "app.tasks.update_exchange_rates", interval, args=[schedule_name], app=celery)
entry.save()

# Uncomment to use APSShedular
# Scheduling using APS schedular

# schedular = BackgroundScheduler()
# schedular.add_job(id='update_exchange_rates_scheduler', 
#                   func=update_exchange_rates_scheduler, 
#                   trigger='cron', 
#                   hour='1,23')
# schedular.start()
