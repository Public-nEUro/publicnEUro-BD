from uuid import uuid4
import hashlib


def generate_passkey() -> str:
    return str(uuid4())


def hash_passkey(passkey: str) -> bool:
    hash_object = hashlib.sha256()
    hash_object.update(passkey.encode("utf-8"))
    return hash_object.hexdigest()


def check_passkey(passkey: str, hash: str) -> bool:
    return hash_passkey(passkey) == hash
