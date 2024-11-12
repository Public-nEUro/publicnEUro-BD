from flask_marshmallow import Marshmallow, Schema
from marshmallow import fields
from ..database.user import User
from ..database.institution import get_db_institution


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
    email_confirmed_at = fields.DateTime(required=True, allow_none=True)
    approved_at = fields.DateTime(required=True, allow_none=True)
    is_admin = fields.Boolean(required=True)
    institution_id = fields.UUID(required=True)
    institution_name = fields.String(required=True)


def extract_user_info(user: User) -> UserInfo:
    db_institution = get_db_institution(user.institution_id)
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "address": user.address,
        "storage_protection": user.storage_protection,
        "access_protection": user.access_protection,
        "created_at": user.created_at,
        "email_confirmed_at": user.email_confirmed_at,
        "approved_at": user.approved_at,
        "is_admin": user.is_admin,
        "institution_id": db_institution.id,
        "institution_name": db_institution.name,
    }


class IdSchema(Schema):
    id = fields.String(required=True)


class FileSchema(Schema):
    file_name = fields.String(required=True, allow_none=True)
    file_data = fields.String(required=True, allow_none=True)
