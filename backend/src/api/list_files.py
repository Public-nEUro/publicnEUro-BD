from pathlib import Path

from flask_marshmallow import Schema
from marshmallow import fields

from .file_path import resolve_path
from .share_token import decrypt_and_validate_share_token


class ListFilesRequestSchema(Schema):
    token = fields.String(required=True)
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
    token_data = decrypt_and_validate_share_token(request["token"])

    return {"files": list_files_delphi(token_data["dataset_id"], request["path"])}


def get_file_details(p: Path, requested_path: str):
    is_file = p.is_file()
    stat = p.stat()
    return {
        "name": p.name,
        "path": Path(requested_path) / p.name,
        "type": "-" if is_file else "d",
        "modified_time": stat.st_mtime if is_file else None,
        "size_bytes": stat.st_size if is_file else None,
    }


def list_files_delphi(dataset_id: str, path: str):
    abs_path = resolve_path(dataset_id, path)

    return [get_file_details(p, path) for p in sorted(Path(abs_path).iterdir())]
