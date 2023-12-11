from flask import Flask
from flask_apscheduler import APScheduler

"""
Type of Triggers
trigger - cron (day_of_week[mon-sun]), hour = 19, minute - 14
"""

app = Flask(__name__)

schedular = APScheduler()

def job1():
    print("This prints every 5 seconds.")

if __name__ == "__main__":
    schedular.add_job(id='Job 1', func=job1, trigger='interval', seconds = 3)
    schedular.start()
    app.run(debug=True, use_reloader=False)