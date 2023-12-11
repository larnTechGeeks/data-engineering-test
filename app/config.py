from os import environ

BASE_URL = environ.get("XE_BASE_URL")
API_ID = environ.get("API_ID")
API_KEY = environ.get("API_KEY")
DATABASE_URL = environ.get("SQLALCHEMY_DATABASE_URI")