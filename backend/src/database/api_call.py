from uuid import uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSON
from . import db


class ApiCall(db.Model):
    __tablename__ = "api_calls"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True))
    timestamp = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String, nullable=False)
    data = db.Column(JSON(none_as_null=True))


def create_api_call_log(user_id, url, data):
    row = ApiCall()
    row.id = uuid4()
    row.user_id = user_id
    row.timestamp = datetime.now()
    row.url = url
    row.data = data

    db.session.add(row)
    db.session.commit()
