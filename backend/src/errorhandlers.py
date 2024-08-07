from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException
from jwt.exceptions import InvalidTokenError
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask, jsonify


def create_response(status_code, message):
    return jsonify(error=status_code, message=message), status_code


def register_errorhandlers(app: Flask):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        app.logger.exception(e)
        if e.code == 400:
            return create_response(400, str(e))
        if e.code == 401:
            return create_response(401, "Unauthorized")
        if e.code == 403:
            return create_response(403, "Forbidden")
        if e.code == 404:
            return create_response(404, "Not found")
        if e.code == 413:
            return create_response(413, "Content too large")
        return create_response(500, "Internal server error")

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        app.logger.exception(e)
        return create_response(400, str(e))

    @app.errorhandler(InvalidTokenError)
    def handle_token_exception(e):
        app.logger.exception(e)
        return create_response(401, str(e))

    @app.errorhandler(RequestException)
    def handler_connection_error(e):
        app.logger.exception(e)
        return e.response.content, e.response.status_code

    @app.errorhandler(SQLAlchemyError)
    def handler_sql_error(e):
        app.logger.exception(e)
        return create_response(500, "Internal database error")

    @app.errorhandler(FileNotFoundError)
    def file_not_found_error(e):
        app.logger.exception(str(e))
        return create_response(404, "File not found")
