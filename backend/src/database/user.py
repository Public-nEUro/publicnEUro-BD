from datetime import datetime
from typing import Union, List
from sqlalchemy import Column, String, DateTime, UniqueConstraint, Boolean
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
    is_admin = Column(Boolean, nullable=False)

    __table_args__ = (UniqueConstraint("email", name="user_unique_email"),)


def get_user(id: str) -> User:
    return db.session.query(User).get(id)


def approve_user(id: str) -> User:
    user = db.session.query(User).get(id)
    user.approved_at = datetime.now()
    db.session.commit()


def get_users() -> List[User]:
    return db.session.query(User).all()


def get_user_by_email(email: str) -> Union[User, None]:
    return db.session.query(User).filter(User.email == email).first()


def user_exists(email: str) -> bool:
    return get_user_by_email(email) is not None


def create_user(user: User) -> None:
    db.session.add(user)
    db.session.commit()
