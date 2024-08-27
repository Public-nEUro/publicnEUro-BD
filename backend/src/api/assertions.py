from flask import abort
from ..database.user import get_user
from ..auth.token import get_auth_user_id
from ..auth.passkey import check_passkey
from ..captcha import validate_captcha_response


def get_logged_in_user_or_abort():
    user_id = get_auth_user_id()

    if user_id is None:
        abort(401)

    user = get_user(user_id)

    if user is None:
        abort(404)

    return user


def get_logged_in_admin_or_abort():
    user = get_logged_in_user_or_abort()

    if not user.is_admin:
        abort(403)


def assert_correct_approver_passkey(user_id, passkey):
    user = get_user(user_id)

    if not check_passkey(passkey, user.approver_passkey_hash):
        abort(403)


def assert_correct_captcha_response(captcha_response):
    if not validate_captcha_response(captcha_response):
        abort(403)
