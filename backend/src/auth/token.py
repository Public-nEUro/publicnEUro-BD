from typing import Union
import os
import jwt
from datetime import timedelta
from flask import request
from ..datetime import get_now


EXPIRE_HOURS = 8
SKEW_MINUTES = 5


def create_token_from_client_secret(user_id, client_secret):
    iat = get_now()
    nbf = iat - timedelta(minutes=SKEW_MINUTES)
    exp = iat + timedelta(hours=EXPIRE_HOURS)
    iss = "Data Manager Backend"
    aud = "Data Manager Client"
    payload = jwt.encode(
        {
            "iat": iat,
            "nbf": nbf,
            "exp": exp,
            "iss": iss,
            "aud": aud,
            "sub": str(user_id),
        },
        client_secret,
        algorithm="HS256",
    )
    return payload


def get_verified_payload_from_token(token, client_secret):
    unverified_payload = jwt.decode(token, options={"verify_signature": False})
    audience = unverified_payload["aud"]
    verified_payload = jwt.decode(
        token, client_secret, algorithms=["HS256"], audience=audience
    )
    return verified_payload


def create_token(user_id):
    return create_token_from_client_secret(user_id, os.environ["CLIENT_SECRET"])


def get_auth_user_id() -> Union[str, None]:
    try:
        token = request.headers["authorization"].split(" ")[1]
        payload = get_verified_payload_from_token(token, os.environ["CLIENT_SECRET"])
        return payload["sub"]
    except Exception:
        return None
