from flask_marshmallow import Schema
from marshmallow import fields
from ..database.user import get_db_approved_users, get_db_non_approved_users
from .utils import assert_is_admin


class GetUsersRequestSchema(Schema):
    pass


class UserSchema(Schema):
    id = fields.UUID(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    address = fields.String(required=True)


class GetUsersResponseSchema(Schema):
    users = fields.Nested(UserSchema, required=True, many=True)


def db_users_to_response(users):
    return {
        "users": [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "address": user.address,
            }
            for user in users
        ]
    }


def get_approved_users(request: GetUsersRequestSchema) -> GetUsersResponseSchema:
    assert_is_admin()

    return db_users_to_response(get_db_approved_users())


def get_non_approved_users(request: GetUsersRequestSchema) -> GetUsersResponseSchema:
    assert_is_admin()

    return db_users_to_response(get_db_non_approved_users())
