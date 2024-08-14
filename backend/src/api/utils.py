from flask import abort
from ..database.user import get_user
from ..auth.token import get_auth_user_id, assert_is_logged_in


def assert_is_admin():
    assert_is_logged_in()

    user_id = get_auth_user_id()

    if not get_user(user_id).is_admin:
        abort(403)
