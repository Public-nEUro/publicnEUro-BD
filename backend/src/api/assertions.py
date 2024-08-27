from flask import abort
from ..database.user import get_user
from ..auth.token import get_auth_user_id
from ..auth.password import check_passkey


def assert_is_logged_in():
    if get_auth_user_id() is None:
        abort(401)


def assert_is_admin():
    user_id = get_auth_user_id()

    if user_id is None:
        abort(401)

    if not get_user(user_id).is_admin:
        abort(403)


def assert_correct_approver_passkey(user_id, passkey):
    user = get_user(user_id)

    if not check_passkey(passkey, user.approver_passkey_hash):
        abort(403)
