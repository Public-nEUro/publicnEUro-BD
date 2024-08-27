from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import EmptySchema, UserInfo, extract_user_info
from .assertions import get_logged_in_user_or_abort
from ..database.user import get_user_from_approver_passkey_hash
from ..auth.passkey import hash_passkey


def get_user_info(request: EmptySchema) -> UserInfo:
    user = get_logged_in_user_or_abort()

    return extract_user_info(user)


class GetUserInfoFromPasskeyRequestSchema(Schema):
    passkey = fields.String(required=True)


def get_user_info_from_passkey(
    request: GetUserInfoFromPasskeyRequestSchema,
) -> UserInfo:
    passkey_hash = hash_passkey(request["passkey"])

    user = get_user_from_approver_passkey_hash(passkey_hash)

    if user is None:
        abort(404)

    return extract_user_info(user)
