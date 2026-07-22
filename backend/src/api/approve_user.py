from flask_marshmallow import Schema
from marshmallow import fields

from ..database.user import (
    approve_user as approve_user_in_db,
)
from ..database.user import (
    get_user,
)
from ..database.user import (
    reject_user as reject_user_in_db,
)
from ..email import send_approved_email
from .common_schemas import EmptySchema


class ApproveUserRequestSchema(Schema):
    user_id = fields.String(required=True)


def approve_user(request: ApproveUserRequestSchema) -> EmptySchema:
    approve_user_in_db(request["user_id"])
    user = get_user(request["user_id"])
    send_approved_email(user.email)


def reject_user(request: ApproveUserRequestSchema) -> EmptySchema:
    reject_user_in_db(request["user_id"])
