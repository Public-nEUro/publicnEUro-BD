import os
from datetime import datetime, timedelta
from typing import TypedDict

from ..datetime import get_now
from .encryption import decrypt_dict, encrypt_dict


class TokenData(TypedDict):
    created_at: str


def create_token(dataset_id: str) -> str:
    return encrypt_dict(
        os.environ["ENCRYPTION_KEY"],
        {"dataset_id": dataset_id, "created_at": get_now().isoformat()},
    )


def decrypt_token(token: str) -> TokenData:
    return decrypt_dict(
        os.environ["ENCRYPTION_KEY"],
        token,
    )


def validate_token(token_data: TokenData) -> None:
    if get_now() - datetime.fromisoformat(token_data["created_at"]) > timedelta(
        hours=72
    ):
        raise PermissionError("Data access expired")


def decrypt_and_validate_token(token: str) -> TokenData:
    result = decrypt_token(token)
    validate_token(result)
    return result
