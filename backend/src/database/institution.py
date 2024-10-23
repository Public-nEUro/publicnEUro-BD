from typing import List, Union
from uuid import uuid4
import enum
from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, ENUM
from . import db
from .db_util import add_row


class Acceptance(enum.Enum):
    ACCEPT = "ACCEPT"
    DO_NOT_ACCEPT = "DO_NOT_ACCEPT"


class Institution(db.Model):
    __tablename__ = "institution"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    country_id = Column(UUID(as_uuid=True), db.ForeignKey("country.id"), nullable=True)
    scc_acceptance = Column(ENUM(Acceptance), nullable=True)

    __table_args__ = (UniqueConstraint("name", name="institution_unique_name"),)


def get_db_institutions() -> List[Institution]:
    return db.session.query(Institution).order_by(Institution.name.asc())


def get_db_institution(id: str) -> Union[Institution, None]:
    return db.session.query(Institution).get(id)


def get_institution_by_name(name: str) -> Union[Institution, None]:
    return db.session.query(Institution).filter(Institution.name == name).first()


def create_institution_if_not_exists(name: str) -> None:
    if get_institution_by_name(name) is not None:
        return

    institution = Institution()
    institution.id = uuid4()
    institution.name = name
    institution.contact = ""
    institution.country_id = None
    institution.scc_acceptance = None
    add_row(institution)
