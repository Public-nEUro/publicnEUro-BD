from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields

from ..auth.passkey import hash_passkey
from ..database.user import (
    get_user_by_email_confirmation_passkey_hash,
)
from ..database.user import (
    reset_password as reset_password_in_db,
)
from .common_schemas import EmptySchema


class ResetPasswordWithPasskeyRequestSchema(Schema):
    passkey = fields.String(required=True)
    new_password = fields.String(required=True)


def reset_password_with_passkey(
    request: ResetPasswordWithPasskeyRequestSchema,
) -> EmptySchema:
    user = get_user_by_email_confirmation_passkey_hash(hash_passkey(request["passkey"]))

    if user is None or user.email_confirmed_at is None:
        abort(403)

    reset_password_in_db(user.id, request["new_password"])

    return {}
