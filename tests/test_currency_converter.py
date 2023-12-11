from unittest.mock import patch


@patch('app.utils.currency_converter.requests.get')
def test_convert_from_success(mock_get, currency_client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "terms": "http://www.xe.com/legal/dfs.php",
        "privacy": "http://www.xe.com/privacy.php",
        "from": "USD",
        "amount": 1,
        "timestamp": "2023-12-10T00:00:00Z",
        "to": [
            {"quotecurrency": "KES", "mid": 153.4247767165},
            {"quotecurrency": "UGX", "mid": 3804.303660686}
        ]
    }

    response = currency_client.convert_from()
    assert response['success'] is True
    assert 'to' in response['data']

@patch('app.utils.currency_converter.requests.get')
def test_convert_from_failure(mock_get, currency_client):
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = {
        "code": 7,
        "message": "No KES, UGX found on 2023-12-10T06:53:58Z",
        "documentation_url": "https://xecdapi.xe.com/docs/v1/"
    }

    response = currency_client.convert_from()
    assert response['success'] is False
    assert 'message' in response['data']