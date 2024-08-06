from typing import Tuple
import secrets
import hashlib
from flask_sqlalchemy import Model
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID


class User(Model):
    id = Column(UUID, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    approved_at = Column(DateTime, nullable=False)
    password_hash = Column(String(64))
    password_salt = Column(String(32))


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
