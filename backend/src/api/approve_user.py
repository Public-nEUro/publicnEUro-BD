from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import EmptySchema
from ..database.user import (
    approve_user as approve_user_in_db,
    reject_user as reject_user_in_db,
)
from .assertions import get_logged_in_admin_or_abort, assert_correct_approver_passkey


class ApproveUserRequestSchema(Schema):
    user_id = fields.String(required=True)


def approve_user(request: ApproveUserRequestSchema) -> EmptySchema:
    get_logged_in_admin_or_abort()

    approve_user_in_db(request["user_id"])


def reject_user(request: ApproveUserRequestSchema) -> EmptySchema:
    get_logged_in_admin_or_abort()

    reject_user_in_db(request["user_id"])


class ApproveUserWithPasskeyRequestSchema(Schema):
    user_id = fields.String(required=True)
    passkey = fields.String(required=True)


def approve_user_with_passkey(
    request: ApproveUserWithPasskeyRequestSchema,
) -> EmptySchema:
    assert_correct_approver_passkey(request["user_id"], request["passkey"])

    approve_user_in_db(request["user_id"])


def reject_user_with_passkey(
    request: ApproveUserWithPasskeyRequestSchema,
) -> EmptySchema:
    assert_correct_approver_passkey(request["user_id"], request["passkey"])

    reject_user_in_db(request["user_id"])
