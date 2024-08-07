from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from ..database import db
from ..auth.password import check_password
from ..auth.user import User
from ..auth.token import create_token


class LoginRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class LoginResponseSchema(Schema):
    token = fields.String(required=True)


def login(request: LoginRequestSchema) -> LoginResponseSchema:
    user: User = db.session.query(User).filter(User.email == request["email"]).first()

    if user is None:
        abort(401)

    if not check_password(request["password"], user.password_hash, user.password_salt):
        abort(401)

    return {"token": create_token(user.id)}
