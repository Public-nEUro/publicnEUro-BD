from os import environ

LOG_LEVEL = "INFO"

SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
SQLALCHEMY_TRACK_MODIFICATIONS = False

OPENAPI_SERVER_LIST = [
    {"url": "http://localhost/", "description": "Local"},
]

UI_PATH = "/swagger/ui"
