from typing import List, Optional, Union

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from . import db


class Scc(db.Model):
    __tablename__ = "scc"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_data = Column(String, nullable=False)  # base 64
    timestamp = Column(DateTime(timezone=True), nullable=False)


def get_db_sccs() -> List[Scc]:
    return (
        db.session.query(*[c for c in Scc.__table__.c if c.name != "file_data"])
        .order_by(Scc.file_name.asc())
        .all()
    )


def get_db_scc(id: Optional[str]) -> Union[Scc, None]:
    if id is None:
        return None
    return db.session.query(Scc).get(id)
