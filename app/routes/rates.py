import datetime
import json
from sqlalchemy import func
from flask import request, Blueprint, jsonify
from app.utils.currency_converter import CurrencyClient
from app.extensions import db
from app.models import CurrencyExchangeRate
from app.config import *
from flask import current_app

rates = Blueprint("rates", __name__)

@rates.route("/v1/rates", methods=['GET'])
def get_rates():
    params = request.args.get('currency')
    try:
        if params:
            rates = CurrencyExchangeRate.query.filter_by(currency_to=params.upper()).all()
            rates_json = json.dumps([rate.to_dict() for rate in rates], indent=4)
        else:
            rates = CurrencyExchangeRate.query.all()
            rates_json = json.dumps([rate.to_dict() for rate in rates], indent=4)
        return current_app.response_class(rates_json, content_type='application/json'), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@rates.route("/v1/rates/update",  methods=["POST", "GET"])
def update():
    converter = CurrencyClient(
        base_url=BASE_URL,
        api_id=API_ID,
        api_key=API_KEY,
        to_currencies= ['NGN', 'GHS', 'KES', 'UGX', 'MAD', 'XOF', 'EGP']
    )

    res = converter.convert_from()
    print("response")
    print(res)

    if res.get("success"):
        data = res.get("data")
        timestamp = datetime.datetime.now(datetime.UTC)
        today = timestamp.date()
        try:
            for currency in data['to']:
                currency_to = currency['quotecurrency']
                existing_rate = CurrencyExchangeRate.query.filter(
                    CurrencyExchangeRate.currency_to == currency_to,
                    func.date(CurrencyExchangeRate.timestamp) == today
                ).first()

                if existing_rate:
                    print("Existing")
                    existing_rate.USD_to_currency_rate = 1 / currency['mid']
                    existing_rate.currency_to_USD_rate = currency['mid']
                else:
                    new_rate = CurrencyExchangeRate(
                        timestamp=datetime.datetime.utcfromtimestamp(0),
                        currency_from=data['from'],
                        USD_to_currency_rate=1 / currency['mid'],
                        currency_to_USD_rate=currency['mid'],
                        currency_to=currency_to
                    )
                    db.session.add(new_rate)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
        finally:
            db.session.remove()

        return jsonify({"success":True})

    return jsonify({"success":False}), 400



