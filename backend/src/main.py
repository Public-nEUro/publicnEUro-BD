from swagger_ui import api_doc
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify
from flask_cors import CORS
from logging.config import dictConfig
from .database import db
from .api.schema import ma
from .errorhandlers import register_errorhandlers
from .api import init_endpoints as init_api
from .config import LOG_LEVEL

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": "false",
        "formatters": {
            "basic": {
                "class": "logging.Formatter",
                "format": "%(asctime)s : %(levelname)s : %(name)s : %(message)s",
                "datefmt": "%d-%m-%Y %H:%M:%S",
            }
        },
        "handlers": {
            "log": {
                "class": "logging.StreamHandler",
                "level": LOG_LEVEL,
                "formatter": "basic",
                "stream": "ext://sys.stdout",
            },
            "sql": {
                "class": "logging.StreamHandler",
                "level": LOG_LEVEL,
                "formatter": "basic",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "sqlalchemy.engine": {
                "level": LOG_LEVEL,
                "handlers": ["sql"],
                "propagate": False,
            },
            "src.main": {"level": LOG_LEVEL, "handlers": ["log"]},
        },
    }
)


def api_spec(app: Flask):
    spec = APISpec(
        title="Usage API",
        version="0.1.0",
        openapi_version="3.0.0",
        servers=app.config["OPENAPI_SERVER_LIST"],
        security=[{"JWTbearer": []}],
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    spec.components.security_scheme("JWTbearer", jwt_scheme)

    with app.test_request_context():
        for key, value in app.view_functions.items():
            if key.startswith("api_"):
                spec.path(view=value)
    return spec.to_dict()


def create_app(name):
    app = Flask(name)
    app.config.from_pyfile("config.py")
    register_errorhandlers(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    ma.init_app(app)

    init_api(app)

    @app.route("/swagger/swagger.json")
    def openAPIdoc():
        return jsonify(api_spec(app))

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def default_response(path):
        return f"/{path} is not implemented"

    with app.app_context():
        db.create_all()

    return app


app = create_app(__name__)

if "UI_PATH" in app.config:
    api_doc(app, config=api_spec(app), url_prefix=app.config["UI_PATH"])

if __name__ == "__main__":
    app.run(port=5000)
