from typing import List
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from . import db
from ..auth.token import get_auth_user_id


MAX_STR_LENGTH = 1024


def make_json_friendly(obj):
    if obj is None:
        return None
    if isinstance(obj, str):
        length = len(obj)
        excess = length - MAX_STR_LENGTH
        if excess > 0:
            return obj[:MAX_STR_LENGTH] + f" ({excess} symbols have been truncated)"
        return obj
    if isinstance(obj, (int, float, bool)):
        return obj
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {make_json_friendly(k): make_json_friendly(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_json_friendly(v) for v in obj]
    return str(obj)


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

    latest_row = (
        db.session.query(History)
        .filter(History.object_id == object_id)
        .order_by(History.timestamp.desc())
        .first()
    )
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


def get_db_history(offset: int, limit: int) -> List[History]:
    return (
        db.session.query(History)
        .order_by(History.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_db_history_count() -> int:
    return db.session.query(History).count()
