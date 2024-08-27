from typing import Tuple
import secrets
import hashlib


def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt=bytes.fromhex(salt), iterations=1000
    ).hex()


def gen_hash_and_salt(password: str) -> Tuple[str, str]:
    salt = secrets.token_bytes(16).hex()
    hash = hash_password(password, salt)
    return hash, salt


def check_password(password: str, hash: str, salt: str) -> bool:
    return hash_password(password, salt) == hash
