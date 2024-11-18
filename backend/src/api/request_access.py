from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from ..auth.token import get_auth_user_id
from ..datetime import get_now
from ..database.user_dataset import UserDataset
from ..dataset_access_info import get_access_info
from ..database.db_util import add_row


class RequestAccessRequestSchema(Schema):
    dataset_id = fields.String(required=True)
    accept_dua = fields.Boolean(required=True)


class RequestAccessResponseSchema(Schema):
    pass


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

    user_dataset = UserDataset()
    user_dataset.user_id = user_id
    user_dataset.dataset_id = request["dataset_id"]
    user_dataset.access_requested_at = get_now()
    user_dataset.user_accepted_dua_at = get_now()
    user_dataset.access_granted_by_admin_at = None
    add_row(user_dataset)

    return {}
