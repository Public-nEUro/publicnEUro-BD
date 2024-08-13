from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from ..database.user import get_user, approve_user as approve_user_in_db
from ..auth.token import get_auth_user_id, assert_is_logged_in


class ApproveUserRequestSchema(Schema):
    user_id = fields.String(required=True)


class ApproveUserResponseSchema(Schema):
    pass


def approve_user(request: ApproveUserRequestSchema) -> ApproveUserResponseSchema:
    assert_is_logged_in()

    user_id = get_auth_user_id()

    if not get_user(user_id).is_admin:
        abort(403)

    approve_user_in_db(request["user_id"])
