from flask_marshmallow import Schema
from marshmallow import fields
from ..dataset_access_check import (
    AccessRequestStatus,
    get_access_request_status,
    access_request_status_to_message,
    perform_access_check,
)


class CheckAccessRequestSchema(Schema):
    user_id = fields.String(required=True)
    dataset_id = fields.String(required=True)


class CheckAccessResponseSchema(Schema):
    status_message = fields.String(required=True)


def check_access(request: CheckAccessRequestSchema) -> CheckAccessResponseSchema:
    access_request_status = get_access_request_status(
        request["user_id"], request["dataset_id"]
    )

    status_message, _ = perform_access_check(
        request["user_id"],
        request["dataset_id"],
        access_request_status is AccessRequestStatus.ACCESSIBLE,
        access_request_status_to_message[access_request_status],
        True,
    )

    return {"status_message": status_message}
