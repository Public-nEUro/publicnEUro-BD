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


def check_password(password: str, hash: str, salt: str) -> str:
    return hash_password(password, salt) == hash


def hash_passkey(passkey: str) -> str:
    hash_object = hashlib.sha256()
    hash_object.update(passkey.encode("utf-8"))
    return hash_object.hexdigest()


def check_passkey(passkey: str, hash: str) -> str:
    return hash_passkey(passkey) == hash
