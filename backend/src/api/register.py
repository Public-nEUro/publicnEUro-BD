import os
from uuid import uuid4
from datetime import datetime
import pytz
from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from ..auth.password import gen_hash_and_salt, hash_passkey
from ..database.user import User, create_user, user_exists
from ..mail import send_mail
from ..captcha import validate_captcha_response


class RegisterRequestSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    address = fields.String(required=True)
    password = fields.String(required=True)
    captcha_response = fields.String(required=True)


class RegisterResponseSchema(Schema):
    pass


def register(request: RegisterRequestSchema) -> RegisterResponseSchema:
    if not validate_captcha_response(request["captcha_response"]):
        abort(403)

    if user_exists(request["email"]):
        return

    hash, salt = gen_hash_and_salt(request["password"])
    approver_passkey = str(uuid4())
    approver_passkey_hash = hash_passkey(approver_passkey)

    user = User()
    user.id = uuid4()
    user.first_name = request["first_name"]
    user.last_name = request["last_name"]
    user.email = request["email"]
    user.address = request["address"]
    user.created_at = datetime.now(tz=pytz.timezone("UTC"))
    user.updated_at = datetime.now(tz=pytz.timezone("UTC"))
    user.approved_at = None
    user.password_hash = hash
    user.password_salt = salt
    user.is_admin = False
    user.approver_passkey_hash = approver_passkey_hash

    send_mail(
        "registration",
        {"link": f"{os.environ['BACKEND_URL']}/approval/{approver_passkey}"},
        os.environ["APPROVER_EMAIL"],
    )

    create_user(user)
