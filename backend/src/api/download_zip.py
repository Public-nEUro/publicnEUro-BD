import json
import os

import requests
from flask import Response
from flask_marshmallow import Schema
from marshmallow import fields


class PrepareZipRequestSchema(Schema):
    share_auth = fields.String(required=True)
    paths = fields.List(fields.String(required=True), required=True)


class PrepareZipResponseSchema(Schema):
    url = fields.String(required=True)
    file_name = fields.String(required=True)


def prepare_zip(request: PrepareZipRequestSchema) -> PrepareZipResponseSchema:
    url = (
        os.environ["DELPHI_BACKEND_URL"]
        + "/project_management/file_management/download/prepare"
    )
    response = requests.post(
        url,
        json.dumps(
            {
                "authorization_header": None,
                "paths": request["paths"],
                "project_id": None,
                "share_auth": request["share_auth"],
            }
        ),
        verify=True,
        headers={"Content-Type": "application/json"},
    )

    response.raise_for_status()
    res = response.json()

    token = res["url"].rsplit("/", 1)[-1]

    url = os.environ["FRONTEND_URL"] + f"/api/download_zip/{token}"

    return {"url": url, "file_name": res["file_name"]}


def download_zip(token: str):
    url = (
        os.environ["DELPHI_BACKEND_URL"]
        + f"/project_management/file_management/download/download/{token}"
    )
    response = requests.get(url, verify=True, stream=True)

    return Response(
        response.iter_content(chunk_size=8192),
        status=response.status_code,
        content_type=response.headers.get("Content-Type"),
        headers={
            "Content-Disposition": response.headers.get(
                "Content-Disposition", "attachment;"
            )
        },
    )
