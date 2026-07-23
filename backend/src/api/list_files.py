import json
import os

import requests
from flask_marshmallow import Schema
from marshmallow import fields


class ListFilesRequestSchema(Schema):
    share_auth = fields.String(required=True)
    path = fields.String(required=True)


class FileDetails(Schema):
    modified_time = fields.String(required=True, allow_none=True)
    name = fields.String(required=True)
    path = fields.String(required=True)
    size_bytes = fields.Integer(required=True, allow_none=True)
    type = fields.String(required=True)


class ListFilesResponseSchema(Schema):
    files = fields.Nested(FileDetails, required=True, many=True)


def list_files(request: ListFilesRequestSchema) -> ListFilesResponseSchema:
    return {"files": list_files_delphi(request["share_auth"], request["path"])}


def list_files_delphi(share_auth: str, path: str):
    backend_url = (
        os.environ["DELPHI_BACKEND_URL"] + "/project_management/file_management/list"
    )
    payload = {
        "authorization_header": None,
        "path": path,
        "project_id": None,
        "share_auth": share_auth,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        backend_url, json.dumps(payload), verify=True, headers=headers
    )
    response.raise_for_status()
    files = response.json()["files"]
    return [
        {
            "modified_time": file["modified_time"],
            "name": file["name"],
            "path": file["path"],
            "size_bytes": file["size_bytes"],
            "type": file["type"],
        }
        for file in files
    ]
