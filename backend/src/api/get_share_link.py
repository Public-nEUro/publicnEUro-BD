from flask import abort, request
from flask_marshmallow import Schema
from marshmallow import fields
from ..auth.password import check_password
from ..database.user import get_user_by_email
from ..database.dataset import get_db_dataset
from ..database.user_dataset import get_db_user_dataset
from ..database.db_util import save_row
from ..dataset_access_check import (
    AccessRequestStatus,
    get_access_request_status,
    access_request_status_to_message,
    perform_access_check,
)
from ..database.api_call import log_api_call


class GetShareLinkRequestSchema(Schema):
    dataset_id = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)


class GetShareLinkResponseSchema(Schema):
    share_link = fields.String(required=True)


def get_auth_user():
    if request.authorization is None:
        return None

    user = get_user_by_email(request.authorization.username)

    if user is None:
        return None

    if not check_password(
        request.authorization.password, user.password_hash, user.password_salt
    ):
        return None

    return user


def get_share_link(dataset_id: str) -> str:
    user = get_auth_user()

    log_api_call(
        user.id if user is not None else None, request.url, {"dataset_id": dataset_id}
    )

    if user is None:
        abort(401)

    dataset = get_db_dataset(dataset_id)
    if dataset is None:
        abort(404)

    user_dataset = get_db_user_dataset(user.id, dataset_id)
    if user_dataset is None:
        abort(403)

    user_dataset.delphi_share_created_at = None
    save_row(user_dataset)

    access_request_status = get_access_request_status(user.id, dataset_id)

    _, share_link = perform_access_check(
        user.id,
        dataset_id,
        access_request_status is AccessRequestStatus.ACCESSIBLE,
        access_request_status_to_message[access_request_status],
        False,
    )

    if share_link is None:
        abort(403)

    return share_link
