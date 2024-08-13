from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from ..database.user import get_user, get_users as get_users_from_db
from ..auth.token import get_auth_user_id, assert_is_logged_in


class GetUsersRequestSchema(Schema):
    pass


class UserSchema(Schema):
    id = fields.UUID(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    address = fields.String(required=True)
    approved = fields.Boolean(required=True)
    is_admin = fields.Boolean(required=True)


class GetUsersResponseSchema(Schema):
    users = fields.Nested(UserSchema, required=True, many=True)


def get_users(request: GetUsersRequestSchema) -> GetUsersResponseSchema:
    assert_is_logged_in()

    user_id = get_auth_user_id()

    if not get_user(user_id).is_admin:
        abort(403)

    users = get_users_from_db()

    return {
        "users": [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "address": user.address,
                "approved": user.approved_at is not None,
                "is_admin": user.is_admin,
            }
            for user in users
        ]
    }
