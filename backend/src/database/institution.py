from typing import List
import enum
from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, ENUM
from . import db


class Acceptance(enum.Enum):
    ACCEPT = "ACCEPT"
    DO_NOT_ACCEPT = "DO_NOT_ACCEPT"


class Institution(db.Model):
    __tablename__ = "institution"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    country_id = Column(UUID(as_uuid=True), db.ForeignKey("country.id"), nullable=False)
    scc_acceptance = Column(ENUM(Acceptance), nullable=False)

    __table_args__ = (UniqueConstraint("name", name="institution_unique_name"),)


def get_db_institutions() -> List[Institution]:
    return db.session.query(Institution).order_by(Institution.name.asc())
