from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from ..auth.token import get_auth_user_id
from ..database.user_dataset import get_db_user_dataset
from ..database.db_util import save_row
from ..dataset_access_check import (
    AccessRequestStatus,
    get_access_request_status,
    access_request_status_to_message,
    perform_access_check,
)


class ResendShareLinkRequestSchema(Schema):
    dataset_id = fields.String(required=True)


class ResendShareLinkResponseSchema(Schema):
    status_message = fields.String(required=True)


def resend_share_link(
    request: ResendShareLinkRequestSchema,
) -> ResendShareLinkResponseSchema:
    user_id = get_auth_user_id()

    user_dataset = get_db_user_dataset(user_id, request["dataset_id"])
    if user_dataset is None:
        abort(404)

    user_dataset.delphi_share_created_at = None
    save_row(user_dataset)

    access_request_status = get_access_request_status(user_id, request["dataset_id"])

    status_message, _ = perform_access_check(
        user_id,
        request["dataset_id"],
        access_request_status is AccessRequestStatus.ACCESSIBLE,
        access_request_status_to_message[access_request_status],
        True,
    )

    return {"status_message": status_message}
