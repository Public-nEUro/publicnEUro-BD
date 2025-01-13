from typing import Union, List
from sqlalchemy import Column, String, DateTime, UniqueConstraint, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import null, false
from . import db
from ..datetime import get_now
from .db_util import add_row, save_row, delete_row
from ..auth.password import gen_hash_and_salt


class User(db.Model):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    institution_id = Column(UUID(as_uuid=True), nullable=False)
    storage_protection = Column(String, nullable=False)
    access_protection = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    email_confirmation_passkey_hash = Column(String(64), nullable=False)
    email_confirmed_at = Column(DateTime(timezone=True), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    password_hash = Column(String(64), nullable=False)
    password_salt = Column(String(32), nullable=False)
    is_admin = Column(Boolean, nullable=False)

    __table_args__ = (UniqueConstraint("email", name="user_unique_email"),)


def get_user(id: str) -> User:
    return db.session.query(User).get(id)


def confirm_email(id: str) -> None:
    user = db.session.query(User).get(id)
    user.email_confirmed_at = get_now()
    user.email_confirmation_passkey_hash = ""
    save_row(user)


def reset_password(id: str, new_password: str) -> None:
    user = db.session.query(User).get(id)
    hash, salt = gen_hash_and_salt(new_password)
    user.password_hash = hash
    user.password_salt = salt
    user.email_confirmation_passkey_hash = ""
    save_row(user)


def approve_user(id: str) -> None:
    user = db.session.query(User).get(id)
    user.approved_at = get_now()
    save_row(user)


def reject_user(id: str) -> None:
    user = db.session.query(User).get(id)
    delete_row(user)


def get_users_query():
    return db.session.query(User).filter(User.is_admin == false())


def get_users_by_id(ids: List[str]) -> User:
    return db.session.query(User).filter(User.id.in_(ids)).all()


def get_db_approved_users() -> List[User]:
    return (
        get_users_query()
        .filter(User.approved_at != null())
        .order_by(User.approved_at.desc())
        .all()
    )


def get_db_non_approved_users() -> List[User]:
    return (
        get_users_query()
        .filter(User.approved_at == null())
        .order_by(User.created_at.desc())
        .all()
    )


def get_user_by_email(email: str) -> Union[User, None]:
    return db.session.query(User).filter(User.email == email).first()


def get_user_by_email_confirmation_passkey_hash(
    email_confirmation_passkey_hash: str,
) -> Union[User, None]:
    return (
        db.session.query(User)
        .filter(User.email_confirmation_passkey_hash == email_confirmation_passkey_hash)
        .first()
    )


def user_exists(email: str) -> bool:
    return get_user_by_email(email) is not None


def create_user(user: User) -> None:
    add_row(user)
