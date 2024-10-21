from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, JSON
from . import db
from ..datetime import get_now
from .db_util import add_row
from .history import make_json_friendly


class ApiCall(db.Model):
    __tablename__ = "api_calls"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True))
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    url = db.Column(db.String, nullable=False)
    data = db.Column(JSON(none_as_null=True))


def log_api_call(user_id, url, data):
    row = ApiCall()
    row.id = uuid4()
    row.user_id = user_id
    row.timestamp = get_now()
    row.url = url
    row.data = make_json_friendly(data)

    add_row(row, False)
