from flask_marshmallow import Schema
from marshmallow import fields
from ..database.user import (
    get_user_by_email_confirmation_passkey_hash,
    confirm_email as confirm_email_in_db,
)
from ..auth.passkey import hash_passkey
from ..email import send_approval_email


class ConfirmEmailWithPasskeyRequestSchema(Schema):
    passkey = fields.String(required=True)


class ConfirmEmailWithPasskeyResponseSchema(Schema):
    message = fields.String(required=True)


def confirm_email_with_passkey(
    request: ConfirmEmailWithPasskeyRequestSchema,
) -> ConfirmEmailWithPasskeyResponseSchema:
    user = get_user_by_email_confirmation_passkey_hash(hash_passkey(request["passkey"]))

    if user is None:
        return {"message": "This user does not exist"}

    if user.email_confirmed_at is not None:
        return {"message": "This email has already been confirmed"}

    confirm_email_in_db(user.id)

    send_approval_email(user.id)

    return {"message": "Your email has been confirmed!"}
