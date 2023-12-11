from celery import shared_task, current_app as celery_app
from redbeat import RedBeatSchedulerEntry
from app.config import *

from app.utils.currency_converter import CurrencyClient

@shared_task(bind=True)
def update_exchange_rates(self, red_beat_name):
    try:
        print("Reading data")
        entry = RedBeatSchedulerEntry.from_key("redbeat:" + red_beat_name, app=celery_app)
        converter = CurrencyClient(
            base_url=BASE_URL,
            api_id=API_ID,
            api_key=API_KEY,
            to_currencies= ['NGN', 'GHS', 'KES', 'UGX', 'MAD', 'XOF', 'EGP']
        )

        res = converter.convert_from()
        print("Result of conversion: ", res)
    except KeyError as e:
        entry = None

    if entry:
        entry.delete()

    return "DONE"