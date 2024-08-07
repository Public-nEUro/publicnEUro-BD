from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from ..database import db


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
