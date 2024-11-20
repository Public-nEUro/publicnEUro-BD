from typing import List
import uuid
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from . import db


class UserDataset(db.Model):
    __tablename__ = "user_dataset"

    user_id = Column(UUID(as_uuid=True), db.ForeignKey("user.id"), primary_key=True)
    dataset_id = Column(String, db.ForeignKey("dataset.id"), primary_key=True)
    access_requested_at = Column(DateTime(timezone=True), nullable=False)
    user_accepted_dua_at = Column(DateTime(timezone=True), nullable=True)
    access_granted_by_admin_at = Column(DateTime(timezone=True), nullable=True)
    delphi_share_created_at = Column(DateTime(timezone=True), nullable=True)


def get_db_user_dataset(user_id: uuid.UUID, dataset_id: str) -> UserDataset:
    return (
        db.session.query(UserDataset)
        .filter(UserDataset.user_id == str(user_id))
        .filter(UserDataset.dataset_id == dataset_id)
        .first()
    )


def get_db_user_datasets(offset: int, limit: int) -> List[UserDataset]:
    return (
        db.session.query(UserDataset)
        .order_by(UserDataset.access_requested_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
