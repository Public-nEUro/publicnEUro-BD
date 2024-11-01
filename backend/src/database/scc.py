from typing import List
from sqlalchemy import Column, String, DateTime
from . import db


class Scc(db.Model):
    __tablename__ = "scc"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_data = Column(String, nullable=False)  # base 64
    timestamp = Column(DateTime, nullable=False)


def get_db_sccs() -> List[Scc]:
    return db.session.query(Scc).all()
