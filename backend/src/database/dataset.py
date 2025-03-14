from typing import List, Union
import enum
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ENUM, UUID
from . import db


class Accessibility(enum.Enum):
    PRIVATE = "PRIVATE"
    EU = "EU"
    EU_AND_ADEQUATE = "EU_AND_ADEQUATE"
    WORLDWIDE = "WORLDWIDE"
    OPEN = "OPEN"


class ApprovalType(enum.Enum):
    OVERSIGHT = "OVERSIGHT"
    AUTOMATED = "AUTOMATED"


class Dataset(db.Model):
    __tablename__ = "dataset"

    id = Column(String, primary_key=True)
    accessibility = Column(ENUM(Accessibility), nullable=False)
    dua_file_name = Column(String, nullable=True)
    dua_file_data = Column(String, nullable=True)  # base 64
    scc_id = Column(UUID(as_uuid=True), db.ForeignKey("scc.id"), nullable=True)
    approval_type = Column(ENUM(ApprovalType), nullable=False)
    delphi_share_url = Column(String, nullable=False)


def get_db_datasets() -> List[Dataset]:
    return db.session.query(
        *[c for c in Dataset.__table__.c if c.name != "dua_file_data"]
    ).order_by(Dataset.id.asc())


def get_db_dataset(id: str) -> Union[Dataset, None]:
    return db.session.query(Dataset).get(id)
