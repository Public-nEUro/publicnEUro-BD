from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import EmptySchema
from ..auth.passkey import generate_passkey_and_hash
from ..database.db_util import save_row
from ..database.user import get_user_by_email
from ..email import send_reset_password_email


class ForgotPasswordRequestSchema(Schema):
    email = fields.Email(required=True)


def forgot_password(request: ForgotPasswordRequestSchema) -> EmptySchema:
    user = get_user_by_email(request["email"])

    if user is None or user.email_confirmed_at is None:
        return {}

    confirmation_passkey, confirmation_hash = generate_passkey_and_hash()

    user.email_confirmation_passkey_hash = confirmation_hash
    save_row(user)

    send_reset_password_email(request["email"], confirmation_passkey)

    return {}
