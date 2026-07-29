import os
import tarfile
import threading
from pathlib import Path

from flask import Response
from flask_marshmallow import Schema
from marshmallow import fields

from .download_token import create_download_token, decrypt_and_validate_download_token
from .file_path import resolve_path
from .share_token import decrypt_and_validate_share_token


class PrepareZipRequestSchema(Schema):
    token = fields.String(required=True)
    paths = fields.List(fields.String(required=True), required=True)


class PrepareZipResponseSchema(Schema):
    url = fields.String(required=True)
    file_name = fields.String(required=True)


def prepare_zip(request: PrepareZipRequestSchema) -> PrepareZipResponseSchema:
    token_data = decrypt_and_validate_share_token(request["token"])

    paths = [resolve_path(token_data["dataset_id"], p) for p in request["paths"]]

    download_token = create_download_token(token_data["dataset_id"], paths)
    url = f"{os.environ['APP_URL']}/api/download_zip/{download_token}"

    return {"url": url, "file_name": get_file_name(paths)}


def tar_gz_stream(paths: list[Path]):
    read_fd, write_fd = os.pipe()

    def writer():
        with os.fdopen(write_fd, "wb") as f:
            with tarfile.open(fileobj=f, mode="w|gz") as tar:
                for p in paths:
                    path = Path(p)
                    tar.add(path, arcname=path.name)

    threading.Thread(target=writer, daemon=True).start()

    with os.fdopen(read_fd, "rb") as f:
        while chunk := f.read(1024 * 64):
            yield chunk


def get_file_name(paths: list[str]):
    return f"{Path(os.path.commonpath([Path(p) for p in paths])).name}.tar.gz"


def download_zip(download_token: str):
    data = decrypt_and_validate_download_token(download_token)

    return Response(
        tar_gz_stream(data["paths"]),
        mimetype="application/gzip",
        headers={
            "Content-Disposition": f"attachment; filename={get_file_name(data['paths'])}"
        },
    )
