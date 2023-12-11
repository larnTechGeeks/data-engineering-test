import json
import responses
from unittest.mock import MagicMock
from app.models import CurrencyExchangeRate

def test_index(client):
    response = client.get("/")
    assert b"<title>Currency APIS</title>" in response.data
    assert b"<li>GET Current Rates making  <b>GET</b> Request to: <b>/v1/rates</b></li>" in response.data

def test_update_route_success(client, app, monkeypatch):
    success_response_data = {
        'terms': "http://www.xe.com/legal/dfs.php",
        'privacy': "http://www.xe.com/privacy.php",
        'from': "USD",
        'amount': 1,
        'timestamp': "2023-12-10T00:00:00Z",
        'to': [
            {'quotecurrency': 'KES', 'mid': 153.4247767165},
            {'quotecurrency': 'UGX', 'mid': 3804.303660686}
        ]
    }

    def mock_convert_from(*args, **kwargs):
        return {'success': True, 'data': success_response_data}


    monkeypatch.setattr('app.utils.currency_converter.CurrencyClient.convert_from', MagicMock(side_effect=mock_convert_from))

    response = client.post('/v1/rates/update')
    assert response.status_code == 200

    data = json.loads(response.data.decode())
    assert data['success'] == True

    with app.app_context():
        assert CurrencyExchangeRate.query.count() == 2
        for currency in success_response_data['to']:
            currency_to = currency['quotecurrency']
            rate_in_db = CurrencyExchangeRate.query.filter_by(currency_to=currency_to).first()

            assert rate_in_db is not None
            assert rate_in_db.USD_to_currency_rate == 1 / currency['mid']
            assert rate_in_db.currency_to_USD_rate == currency['mid']

def test_update_route_failed(client, app, monkeypatch):

    failed_response_data = {
        "code": 7,
        "message": "No KES, UGX found on 2023-12-10T06:53:58Z",
        "documentation_url": "https://xecdapi.xe.com/docs/v1/"
    }

    def mock_convert_from(*args, **kwargs):
        return {'success': False, 'data': failed_response_data}
    
    monkeypatch.setattr('app.utils.currency_converter.CurrencyClient.convert_from', MagicMock(side_effect=mock_convert_from))

    response = client.post('/v1/rates/update')
    assert response.status_code == 400
    
    data = json.loads(response.data.decode())
    assert data.get('success') == False

