import os
from datetime import datetime, timedelta
from typing import TypedDict

from ..datetime import get_now
from .encryption import decrypt_dict, encrypt_dict


class ShareTokenData(TypedDict):
    created_at: str


def create_share_token(dataset_id: str) -> str:
    return encrypt_dict(
        os.environ["ENCRYPTION_KEY"],
        {"dataset_id": dataset_id, "created_at": get_now().isoformat()},
    )


def validate_share_token(token_data: ShareTokenData) -> None:
    if get_now() - datetime.fromisoformat(token_data["created_at"]) > timedelta(
        hours=72
    ):
        raise PermissionError("Data access expired")


def decrypt_and_validate_share_token(token: str) -> ShareTokenData:
    result = decrypt_dict(os.environ["ENCRYPTION_KEY"], token)
    validate_share_token(result)
    return result
