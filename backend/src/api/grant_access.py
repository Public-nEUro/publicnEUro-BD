from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from ..datetime import get_now
from ..database.user_dataset import get_db_user_dataset
from ..database.db_util import save_row
from ..dataset_access_check import (
    AccessRequestStatus,
    get_access_request_status,
    access_request_status_to_message,
    perform_access_check,
)
from .request_access import add_user_dataset_to_db


class GrantAccessRequestSchema(Schema):
    user_id = fields.String(required=True)
    dataset_id = fields.String(required=True)


class GrantAccessResponseSchema(Schema):
    status_message = fields.String(required=True)


def grant_access(request: GrantAccessRequestSchema) -> GrantAccessResponseSchema:
    db_user_dataset = get_db_user_dataset(request["user_id"], request["dataset_id"])

    if db_user_dataset is None:
        add_user_dataset_to_db(request["user_id"], request["dataset_id"])
        db_user_dataset = get_db_user_dataset(request["user_id"], request["dataset_id"])

    if db_user_dataset.access_granted_by_admin_at is not None:
        abort(409)

    db_user_dataset.access_granted_by_admin_at = get_now()
    save_row(db_user_dataset)

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
