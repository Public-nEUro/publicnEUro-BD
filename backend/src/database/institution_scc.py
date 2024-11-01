from typing import List
import uuid
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from . import db


class InstitutionScc(db.Model):
    __tablename__ = "institution_scc"

    institution_id = Column(
        UUID(as_uuid=True), db.ForeignKey("institution.id"), primary_key=True
    )
    scc_id = Column(String, db.ForeignKey("scc.id"), primary_key=True)
    accepted = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, nullable=False)


def get_db_institution_sccs(institution_id: uuid.UUID) -> List[InstitutionScc]:
    return (
        db.session.query(InstitutionScc)
        .filter(InstitutionScc.institution_id == str(institution_id))
        .all()
    )


def get_db_institutions_sccs() -> List[InstitutionScc]:
    return db.session.query(InstitutionScc).all()
