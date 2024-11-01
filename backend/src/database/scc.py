from typing import List
from sqlalchemy import Column, String, LargeBinary, DateTime
from . import db


class Scc(db.Model):
    __tablename__ = "scc"

    id = Column(String, primary_key=True)
    description = Column(String, nullable=False)
    file = Column(LargeBinary, nullable=False)
    timestamp = Column(DateTime, nullable=False)


def get_db_sccs() -> List[Scc]:
    return db.session.query(Scc).all()
