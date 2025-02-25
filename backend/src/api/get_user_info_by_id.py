from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import UserInfo, extract_user_info
from ..database.user import get_user


class GetUserInfoByIdRequestSchema(Schema):
    user_id = fields.String(required=True)


def get_user_info_by_id(request: GetUserInfoByIdRequestSchema) -> UserInfo:
    user = get_user(request["user_id"])

    if user is None:
        abort(404)

    return extract_user_info(user)
