import hashlib


def hash_passkey(passkey: str) -> str:
    hash_object = hashlib.sha256()
    hash_object.update(passkey.encode("utf-8"))
    return hash_object.hexdigest()


def check_passkey(passkey: str, hash: str) -> str:
    return hash_passkey(passkey) == hash
