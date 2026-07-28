import json

from cryptography.fernet import Fernet


def get_fernet(key: str) -> Fernet:
    return Fernet(key.encode())


def encrypt_string(key: str, s: str) -> str:
    return get_fernet(key).encrypt(s.encode()).decode()


def decrypt_string(key: str, s: str) -> str:
    return get_fernet(key).decrypt(s.encode()).decode()


def encrypt_dict(key: str, data: dict) -> str:
    return encrypt_string(key, json.dumps(data))


def decrypt_dict(key: str, encrypted_data: str) -> dict:
    return json.loads(decrypt_string(key, encrypted_data))
