import os
from datetime import datetime, timedelta
from typing import TypedDict

from ..datetime import get_now
from .encryption import decrypt_dict, encrypt_dict


class DownloadTokenData(TypedDict):
    created_at: str


def create_download_token(dataset_id: str, paths: list[str]) -> str:
    download_token_data = {
        "requested_at": get_now().isoformat(),
        "dataset_id": dataset_id,
        "paths": paths,
    }
    return encrypt_dict(os.environ["ENCRYPTION_KEY"], download_token_data)


def validate_download_token(token_data: DownloadTokenData) -> None:
    if get_now() - datetime.fromisoformat(token_data["requested_at"]) > timedelta(
        minutes=1
    ):
        raise PermissionError("Data access expired")


def decrypt_and_validate_download_token(token: str) -> DownloadTokenData:
    result = decrypt_dict(os.environ["ENCRYPTION_KEY"], token)
    validate_download_token(result)
    return result
