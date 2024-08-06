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
