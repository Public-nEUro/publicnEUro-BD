from flask import current_app
from flask_marshmallow import Schema


class TestRequestSchema(Schema):
    pass


class TestResponseSchema(Schema):
    pass


def test_endpoint(request: TestRequestSchema) -> TestResponseSchema:
    current_app.logger.info("test endpoint called")
