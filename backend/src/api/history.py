from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import UserInfo, extract_user_info, PaginationSchema
from ..database.history import get_db_history, get_db_history_count
from ..database.user import get_users_by_id


class EventSchema(Schema):
    id = fields.String(required=True)
    timestamp = fields.DateTime(required=True)
    user_info = fields.Nested(UserInfo, required=True, allow_none=True)
    object_id = fields.Raw(required=True)
    object_data = fields.Raw(required=True)


class GetHistoryResponseSchema(Schema):
    history = fields.Nested(EventSchema, required=True, many=True)
    total = fields.Integer(required=True)


def get_history(request: PaginationSchema) -> GetHistoryResponseSchema:
    history = get_db_history(request["offset"], request["limit"])
    total = get_db_history_count()
    user_ids = list(set([event.user_id for event in history]))
    users = get_users_by_id(user_ids)
    user_dict = {user.id: user for user in users}
    return {
        "history": [
            {
                "id": row.id,
                "timestamp": row.timestamp,
                "user_info": (
                    extract_user_info(user_dict.get(row.user_id))
                    if user_dict.get(row.user_id) is not None
                    else None
                ),
                "object_id": row.object_id,
                "object_data": row.object_data,
            }
            for row in history
        ],
        "total": total,
    }
