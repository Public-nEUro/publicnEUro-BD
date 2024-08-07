from uuid import uuid4
from datetime import datetime
from flask_marshmallow import Schema
from marshmallow import fields
from ..database import db
from ..auth.password import gen_hash_and_salt
from ..auth.user import User


class RegisterRequestSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    address = fields.String(required=True)
    password = fields.String(required=True)


class RegisterResponseSchema(Schema):
    pass


def register(request: RegisterRequestSchema) -> RegisterResponseSchema:
    if db.session.query(User).filter(User.email == request["email"]).count() > 0:
        return

    hash, salt = gen_hash_and_salt(request["password"])

    user = User()
    user.id = uuid4()
    user.first_name = request["first_name"]
    user.last_name = request["last_name"]
    user.email = request["email"]
    user.address = request["address"]
    user.created_at = datetime.now()
    user.updated_at = datetime.now()
    user.approved_at = None
    user.password_hash = hash
    user.password_salt = salt

    db.session.add(user)
    db.session.commit()
