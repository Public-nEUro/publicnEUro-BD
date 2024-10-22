from typing import List
import enum
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID, ENUM
from . import db


class GeoLocation(enum.Enum):
    EU = "EU"
    ADEQUATE = "ADEQUATE"
    OTHER = "OTHER"


class Country(db.Model):
    __tablename__ = "country"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    geo_location = Column(ENUM(GeoLocation), nullable=False)


def get_db_countries() -> List[Country]:
    return (
        db.session.query(Country)
        .order_by(Country.geo_location.asc())
        .order_by(Country.name.asc())
    )
