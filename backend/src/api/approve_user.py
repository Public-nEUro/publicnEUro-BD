from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from .schema import EmptySchema
from ..database.user import (
    get_user,
    approve_user as approve_user_in_db,
    reject_user as reject_user_in_db,
)
from .utils import assert_is_admin
from ..auth.password import check_passkey


class ApproveUserRequestSchema(Schema):
    user_id = fields.String(required=True)


def approve_user(request: ApproveUserRequestSchema) -> EmptySchema:
    assert_is_admin()

    approve_user_in_db(request["user_id"])


def reject_user(request: ApproveUserRequestSchema) -> EmptySchema:
    assert_is_admin()

    reject_user_in_db(request["user_id"])


def assert_correct_passkey(user_id, passkey):
    user = get_user(user_id)

    if not check_passkey(passkey, user.approver_passkey_hash):
        abort(403)


class ApproveUserWithPasskeyRequestSchema(Schema):
    user_id = fields.String(required=True)
    passkey = fields.String(required=True)


def approve_user_with_passkey(
    request: ApproveUserWithPasskeyRequestSchema,
) -> EmptySchema:
    assert_correct_passkey(request["user_id"], request["passkey"])

    approve_user_in_db(request["user_id"])


def reject_user_with_passkey(
    request: ApproveUserWithPasskeyRequestSchema,
) -> EmptySchema:
    assert_correct_passkey(request["user_id"], request["passkey"])

    reject_user_in_db(request["user_id"])
