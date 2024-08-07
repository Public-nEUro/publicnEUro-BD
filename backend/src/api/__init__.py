from flask import request, Response
from .example_endpoint import example_endpoint
from .register import register
from .login import login
from .get_user_info import get_user_info


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


def docstring_file_upload():
    description = "Upload a file"
    doc = f"""
        {description}
        ---
        post:
            description: {description}
            requestBody:
                content:
                    multipart/form-data:
                        schema:
                            type: object
                            properties:
                                file:
                                    type: string
                                    format: binary

            responses:
                200:
                    description: Returns the file id
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    file_id:
                                        type: string
        """

    def _decorator(func):
        func.__doc__ = doc
        return func

    return _decorator


def docstring_file_download(description, input_schema, response_description):
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
                    x-is-file: true
                    content:
                        application/octet-stream:
                            schema:
                                type: object
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


def endpoint(app, function, description="", response_description=""):
    @app.post(f"/{function.__name__}")
    @docstring(
        description,
        function.__annotations__["request"],
        response_description,
        function.__annotations__["return"],
    )
    @change_name(f"api_{function.__name__}")
    def func():
        input_data = function.__annotations__["request"]().load(request.json)
        response = function(input_data)
        return function.__annotations__["return"]().jsonify(response)

    return func


def endpoint_file_upload(app, function, auth):
    @app.post(f"/{function.__name__}")
    @docstring_file_upload()
    @change_name(f"api_{function.__name__}")
    @auth
    def func():
        print(type(request.files["file"]), flush=True)
        input_data = function.__annotations__["request"]().load(
            {"file": request.files["file"]}
        )
        response = function(input_data)
        return function.__annotations__["return"]().jsonify(response)

    return func


def create_response(file, mime_type, file_name):
    return Response(
        file,
        mimetype=mime_type,
        headers={
            "Content-disposition": f"attachment; filename={file_name}",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


def endpoint_file_download(app, function, description, response_description, auth):
    @app.post(f"/{function.__name__}")
    @docstring_file_download(
        description, function.__annotations__["request"], response_description
    )
    @change_name(f"api_{function.__name__}")
    @auth
    def func():
        input_data = function.__annotations__["request"]().load(request.json)
        response = function(input_data)
        return create_response(*response)

    return func


def init_endpoints(app):
    func_list = [example_endpoint, register, login, get_user_info]

    for func in func_list:
        endpoint(app, func)
