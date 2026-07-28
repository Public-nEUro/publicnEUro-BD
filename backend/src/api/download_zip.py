import os
import tarfile
import threading
from datetime import datetime, timedelta
from pathlib import Path

from flask import Response
from flask_marshmallow import Schema
from marshmallow import fields

from ..datetime import get_now
from .encryption import decrypt_dict, encrypt_dict


class PrepareZipRequestSchema(Schema):
    dataset_id = fields.String(required=True)
    token = fields.String(required=True)
    paths = fields.List(fields.String(required=True), required=True)


class PrepareZipResponseSchema(Schema):
    url = fields.String(required=True)
    file_name = fields.String(required=True)


def prepare_zip(request: PrepareZipRequestSchema) -> PrepareZipResponseSchema:
    token = decrypt_dict(
        os.environ["ENCRYPTION_KEY"],
        request["token"],
    )

    if get_now() - datetime.fromisoformat(token["created_at"]) > timedelta(hours=72):
        raise PermissionError("Data access expired")

    paths = [
        str(Path("/datasets") / request["dataset_id"] / p) for p in request["paths"]
    ]

    data = {
        "requested_at": get_now().isoformat(),
        "dataset_id": request["dataset_id"],
        "paths": paths,
    }
    token = encrypt_dict(os.environ["ENCRYPTION_KEY"], data)
    url = f"{os.environ['APP_URL']}/api/download_zip/{token}"

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


def download_zip(token: str):
    data = decrypt_dict(os.environ["ENCRYPTION_KEY"], token)
    if get_now() - datetime.fromisoformat(data["requested_at"]) > timedelta(minutes=1):
        raise PermissionError("Token has expired")

    return Response(
        tar_gz_stream(data["paths"]),
        mimetype="application/gzip",
        headers={
            "Content-Disposition": f"attachment; filename={get_file_name(data['paths'])}"
        },
    )
