from flask_marshmallow import Marshmallow, Schema
from marshmallow import fields


ma = Marshmallow()


class EmptySchema(Schema):
    pass


class UserInfo(Schema):
    id = fields.UUID(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    address = fields.String(required=True)
    storage_protection = fields.String(required=True)
    access_protection = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    approved_at = fields.DateTime(required=True)
    is_admin = fields.Boolean(required=True)


def extract_user_info(user):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "address": user.address,
        "storage_protection": user.storage_protection,
        "access_protection": user.access_protection,
        "created_at": user.created_at,
        "approved_at": user.approved_at,
        "is_admin": user.is_admin,
    }
