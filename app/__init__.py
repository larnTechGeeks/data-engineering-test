from os import environ
from flask import Flask
from app.extensions import db
from app.routes.index import index
from app.routes.rates import rates
from app.config import DATABASE_URL
from app.utils.celery import make_celery


def create_app(dsn = DATABASE_URL):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = dsn
    app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
    app.config["CELERY_CONFIG"] = {
        "broker_url": "redis://localhost", 
        "result_backend": "redis://localhost", 
        "redbeat_redis_url": "redis://localhost"
    }

    # app.config['CELERY_IMPORTS'] = ('.tasks',)

    db.init_app(app)

    app.register_blueprint(index)
    app.register_blueprint(rates)

    celery = make_celery(app)
    celery.set_default()

    # celery.add_periodic_task(update_exchange_rates)

    return app, celery
