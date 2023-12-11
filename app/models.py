import datetime
from app.extensions import db

class CurrencyExchangeRate(db.Model):

    __tablename__ = 'currency_exchange_rates'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    currency_from = db.Column(db.String, nullable=False)
    USD_to_currency_rate = db.Column(db.Float)
    currency_to_USD_rate = db.Column(db.Float)
    currency_to = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<CurrencyExchangeRate(currency_from='{self.currency_from}', currency_to='{self.currency_to}', USD_to_currency_rate={self.USD_to_currency_rate}, currency_to_USD_rate={self.currency_to_USD_rate}, timestamp={self.timestamp})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'currency_from': self.currency_from,
            'USD_to_currency_rate': self.USD_to_currency_rate,
            'currency_to_USD_rate': self.currency_to_USD_rate,
            'currency_to': self.currency_to
        }
