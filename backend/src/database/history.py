from flask import current_app
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from . import db
from ..auth.token import get_auth_user_id


def make_json_friendly(obj):
    if obj is None:
        return None
    if isinstance(obj, (int, float, str, bool)):
        return obj
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: make_json_friendly(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_json_friendly(v) for v in obj]
    return None


class History(db.Model):
    __tablename__ = "history"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), nullable=True)
    object_id = db.Column(JSONB, nullable=False)
    object_data = db.Column(JSONB, nullable=True)


def add_history_row(object_id, object_data):
    object_id = make_json_friendly(object_id)
    object_data = make_json_friendly(object_data)

    user_id = get_auth_user_id()

    current_app.logger.info("qwe")
    current_app.logger.info(object_id)
    latest_row = (
        db.session.query(History)
        .filter(History.object_id == object_id)
        .order_by(History.timestamp.desc())
        .first()
    )
    current_app.logger.info(latest_row)
    if (
        latest_row is not None
        and str(latest_row.user_id) == str(user_id)
        and latest_row.object_data == object_data
    ):
        return

    row = History()
    row.id = uuid.uuid4()
    row.timestamp = datetime.now()
    row.user_id = user_id
    row.object_id = object_id
    row.object_data = object_data
    db.session.add(row)
    db.session.commit()
