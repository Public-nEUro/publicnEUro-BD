from flask_marshmallow import Schema
from marshmallow import fields
from ..database.user import get_user
from ..auth.token import get_auth_user_id, assert_is_logged_in


class GetUserInfoRequestSchema(Schema):
    pass


class GetUserInfoResponseSchema(Schema):
    id = fields.UUID(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    address = fields.String(required=True)
    approved = fields.Boolean(required=True)


def get_user_info(request: GetUserInfoRequestSchema) -> GetUserInfoResponseSchema:
    assert_is_logged_in()

    user_id = get_auth_user_id()

    user = get_user(user_id)

    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "address": user.address,
        "approved": user.approved_at is not None
    }
