from typing import Union
from sqlalchemy import Column, String, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from . import db


class User(db.Model):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    approved_at = Column(DateTime, nullable=True)
    password_hash = Column(String(64), nullable=False)
    password_salt = Column(String(32), nullable=False)

    __table_args__ = (UniqueConstraint("email", name="user_unique_email"),)


def get_user(id: str) -> User:
    return db.session.query(User).get(id)


def get_user_by_email(email: str) -> Union[User, None]:
    return db.session.query(User).filter(User.email == email).first()


def user_exists(email: str) -> bool:
    return get_user_by_email(email) is not None


def create_user(user: User) -> None:
    db.session.add(user)
    db.session.commit()
