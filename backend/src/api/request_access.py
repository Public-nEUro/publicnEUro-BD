from flask import abort, current_app
from flask_marshmallow import Schema
from marshmallow import fields
from requests import HTTPError
from ..auth.token import get_auth_user_id
from ..datetime import get_now
from ..database.user_dataset import UserDataset, get_db_user_dataset
from ..database.user import get_user
from ..database.dataset import get_db_dataset
from ..dataset_access_info import get_access_info
from ..database.db_util import add_row
from ..dataset_access_check import is_allowed_to_access_data, perform_access_check
from ..delphi_share import create_delphi_share


class RequestAccessRequestSchema(Schema):
    dataset_id = fields.String(required=True)
    accept_dua = fields.Boolean(required=True)


class RequestAccessResponseSchema(Schema):
    status_message = fields.String(required=True)


def add_user_dataset_to_db(user_id: str, dataset_id: str):
    user_dataset = UserDataset()
    user_dataset.user_id = user_id
    user_dataset.dataset_id = dataset_id
    user_dataset.access_requested_at = get_now()
    user_dataset.user_accepted_dua_at = get_now()
    user_dataset.access_granted_by_admin_at = None
    user_dataset.delphi_share_created = None
    add_row(user_dataset)


def request_access(request: RequestAccessRequestSchema) -> RequestAccessResponseSchema:
    user_id = get_auth_user_id()
    access_info = get_access_info(user_id, request["dataset_id"])

    if access_info["needs_to_log_in"]:
        abort(401)

    if access_info["needs_to_confirm_email"]:
        abort(403)

    if access_info["needs_to_be_approved"]:
        abort(403)

    if access_info["has_rejected_scc"]:
        abort(403)

    if not access_info["is_accessible_in_country"]:
        abort(403)

    if not request["accept_dua"]:
        abort(403)

    user = get_user(user_id)

    if user is None:
        abort(404)

    dataset = get_db_dataset(request["dataset_id"])

    if dataset is None:
        abort(404)

    existing_user_dataset = get_db_user_dataset(user_id, request["dataset_id"])
    if existing_user_dataset is None:
        add_user_dataset_to_db(user_id, request["dataset_id"])

    status_message = perform_access_check(user_id, request["dataset_id"])

    return {"status_message": status_message}
