from typing import List
from flask_marshmallow import Schema
from marshmallow import fields
from ..database.user import User, get_db_approved_users, get_db_non_approved_users
from .assertions import get_logged_in_admin_or_abort
from .common_schemas import UserInfo, extract_user_info


class GetUsersRequestSchema(Schema):
    pass


class GetUsersResponseSchema(Schema):
    users = fields.Nested(UserInfo, required=True, many=True)


def db_users_to_response(users: List[User]):
    return {"users": [extract_user_info(user) for user in users]}


def get_approved_users(request: GetUsersRequestSchema) -> GetUsersResponseSchema:
    get_logged_in_admin_or_abort()

    return db_users_to_response(get_db_approved_users())


def get_non_approved_users(request: GetUsersRequestSchema) -> GetUsersResponseSchema:
    get_logged_in_admin_or_abort()

    return db_users_to_response(get_db_non_approved_users())
