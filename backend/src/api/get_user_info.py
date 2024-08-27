from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import EmptySchema
from .assertions import get_logged_in_user_or_abort
from ..database.user import get_user_from_approver_passkey_hash
from ..auth.passkey import hash_passkey


def db_user_to_response(user):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "address": user.address,
        "storage_protection": user.storage_protection,
        "access_protection": user.access_protection,
        "approved": user.approved_at is not None,
        "is_admin": user.is_admin,
    }


class GetUserInfoResponseSchema(Schema):
    id = fields.UUID(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    address = fields.String(required=True)
    storage_protection = fields.String(required=True)
    access_protection = fields.String(required=True)
    approved = fields.Boolean(required=True)
    is_admin = fields.Boolean(required=True)


def get_user_info(request: EmptySchema) -> GetUserInfoResponseSchema:
    user = get_logged_in_user_or_abort()

    return db_user_to_response(user)


class GetUserInfoFromPasskeyRequestSchema(Schema):
    passkey = fields.String(required=True)


def get_user_info_from_passkey(
    request: GetUserInfoFromPasskeyRequestSchema,
) -> GetUserInfoResponseSchema:
    passkey_hash = hash_passkey(request["passkey"])

    user = get_user_from_approver_passkey_hash(passkey_hash)

    if user is None:
        abort(404)

    return db_user_to_response(user)
