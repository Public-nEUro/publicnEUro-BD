from flask import request, current_app
from .register import register
from .login import login
from .get_user_info import get_user_info
from .get_user_info_from_passkey import get_user_info_from_passkey
from .get_users import get_approved_users, get_non_approved_users
from .confirm_email import confirm_email_with_passkey
from .approve_user import (
    approve_user,
    reject_user,
    approve_user_with_passkey,
    reject_user_with_passkey,
)
from .country import add_country, get_countries
from .institution import add_institution, get_institutions, update_institution
from .scc import add_scc, get_sccs
from .dataset import get_datasets, update_dataset
from .user_dataset import get_user_dataset
from .history import get_history
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


def endpoint(app, function, description="", response_description=""):
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
        response = function(input_data)
        return function.__annotations__["return"]().jsonify(response)

    return func


def init_endpoints(app):
    func_list = [
        register,
        login,
        get_user_info,
        get_user_info_from_passkey,
        get_approved_users,
        get_non_approved_users,
        approve_user,
        reject_user,
        confirm_email_with_passkey,
        approve_user_with_passkey,
        reject_user_with_passkey,
        add_country,
        get_countries,
        add_institution,
        get_institutions,
        update_institution,
        get_datasets,
        update_dataset,
        get_user_dataset,
        get_history,
        add_scc,
        get_sccs,
    ]

    for func in func_list:
        endpoint(app, func)
