from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import UserInfo, extract_user_info
from ..database.user import get_user_from_approver_passkey_hash
from ..auth.passkey import hash_passkey


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
