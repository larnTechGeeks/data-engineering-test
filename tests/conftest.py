from os import environ
import pytest
from app import create_app, db
from app.config import *
from app.utils.currency_converter import CurrencyClient 

@pytest.fixture()
def app():
    app, _ = create_app("sqlite://")
    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
   return app.test_client() 

@pytest.fixture
def currency_client():
    return CurrencyClient(BASE_URL, API_ID, API_KEY,  ['KES', 'UGX'])

