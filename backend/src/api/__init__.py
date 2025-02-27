import enum
from flask import request, current_app
from .register import register
from .login import login
from .forgot_password import forgot_password
from .reset_password import reset_password_with_passkey
from .get_user_info import get_user_info
from .get_user_info_by_id import get_user_info_by_id
from .get_users import get_approved_users, get_non_approved_users
from .confirm_email import confirm_email_with_passkey
from .approve_user import approve_user, reject_user
from .country import add_country, delete_country, get_countries
from .institution import get_institutions, update_institution
from .scc import add_scc, get_sccs, get_scc
from .dataset import (
    get_datasets,
    get_dataset,
    get_delphi_share_url,
    get_dataset_dua,
    update_dataset,
)
from .user_dataset import (
    get_user_dataset,
    get_user_datasets,
    get_user_datasets_for_dataset,
)
from .request_access import request_access
from .resend_share_link import resend_share_link
from .grant_access import grant_access
from .delete_access_request import delete_access_request
from .check_access import check_access
from .history import get_history
from .assertions import get_logged_in_admin_or_abort, get_logged_in_user_or_abort
from ..auth.token import get_auth_user_id
from ..database.api_call import log_api_call


def docstring(description, input_schema, response_description, response_schema):
    doc = f"""
        {description}
        ---
        post:
            description: {description}
            requestBody:
                content:
                    application/json:
                        schema: {input_schema.__name__}
            responses:
                200:
                    description: {response_description}
                    content:
                        application/json:
                            schema: {response_schema.__name__}
        """

    def _decorator(func):
        func.__doc__ = doc
        return func

    return _decorator


def change_name(name):
    def _decorator(func):
        func.__name__ = name
        return func

    return _decorator


def hide_password(data):
    if not isinstance(data, dict):
        return data

    try:
        result = {**data}
        if "password" in result:
            result["password"] = "__HIDDEN__"
        if "share_auth" in result:
            result["share_auth"] = "__HIDDEN__"
        return result
    except Exception as e:
        current_app.logger.exception(str(e))
        return data


class AuthType(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    ALL = "ALL"


def assert_auth(auth_type: AuthType):
    if auth_type == AuthType.USER:
        get_logged_in_user_or_abort()
    if auth_type == AuthType.ADMIN:
        get_logged_in_admin_or_abort()


def endpoint(
    app, function, auth_type: AuthType, description="", response_description=""
):
    @app.post(f"/api/{function.__name__}")
    @docstring(
        description,
        function.__annotations__["request"],
        response_description,
        function.__annotations__["return"],
    )
    @change_name(f"api_{function.__name__}")
    def func():
        input_data = function.__annotations__["request"]().load(request.json)
        log_api_call(get_auth_user_id(), request.url, hide_password(input_data))
        assert_auth(auth_type)
        response = function(input_data)
        return function.__annotations__["return"]().jsonify(response)

    return func


def init_endpoints(app):
    func_list = [
        [register, AuthType.ALL],
        [login, AuthType.ALL],
        [forgot_password, AuthType.ALL],
        [reset_password_with_passkey, AuthType.ALL],
        [get_user_info, AuthType.USER],
        [get_user_info_by_id, AuthType.ADMIN],
        [get_approved_users, AuthType.ADMIN],
        [get_non_approved_users, AuthType.ADMIN],
        [approve_user, AuthType.ADMIN],
        [reject_user, AuthType.ADMIN],
        [confirm_email_with_passkey, AuthType.ALL],
        [add_country, AuthType.ADMIN],
        [delete_country, AuthType.ADMIN],
        [get_countries, AuthType.ADMIN],
        [get_institutions, AuthType.ALL],
        [update_institution, AuthType.ADMIN],
        [get_datasets, AuthType.ADMIN],
        [get_dataset, AuthType.ALL],
        [get_delphi_share_url, AuthType.ALL],
        [get_dataset_dua, AuthType.USER],
        [update_dataset, AuthType.ADMIN],
        [get_user_dataset, AuthType.USER],
        [get_user_datasets, AuthType.ADMIN],
        [get_user_datasets_for_dataset, AuthType.ADMIN],
        [request_access, AuthType.USER],
        [resend_share_link, AuthType.USER],
        [grant_access, AuthType.ADMIN],
        [delete_access_request, AuthType.ADMIN],
        [check_access, AuthType.ADMIN],
        [get_history, AuthType.ADMIN],
        [add_scc, AuthType.ADMIN],
        [get_sccs, AuthType.ADMIN],
        [get_scc, AuthType.ADMIN],
    ]

    for func, auth_type in func_list:
        endpoint(app, func, auth_type)
