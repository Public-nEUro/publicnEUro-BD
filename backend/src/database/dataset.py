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
    PUBLIC = "PUBLIC"


class ApprovalType(enum.Enum):
    OVERSIGHT = "OVERSIGHT"
    AUTOMATED = "AUTOMATED"


class Dataset(db.Model):
    __tablename__ = "dataset"

    id = Column(String, primary_key=True)
    accessibility = Column(ENUM(Accessibility), nullable=False)
    dua_file_name = Column(String, nullable=True)
    dua_file_data = Column(String, nullable=True)  # base 64
    dua_approval_type = Column(ENUM(ApprovalType), nullable=False)
    scc_id = Column(UUID(as_uuid=True), nullable=True)
    scc_approval_type = Column(ENUM(ApprovalType), nullable=False)


def get_db_datasets() -> List[Dataset]:
    return db.session.query(Dataset).order_by(Dataset.id.asc())


def get_db_dataset(id: str) -> Union[Dataset, None]:
    return db.session.query(Dataset).get(id)
