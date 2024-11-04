from typing import List, Dict
from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import UserInfo, extract_user_info
from ..database.history import History, get_db_history
from ..database.user import User, get_users_by_id


class EventSchema(Schema):
    id = fields.String(required=True)
    timestamp = fields.DateTime(required=True)
    user_info = fields.Nested(UserInfo, required=True, allow_none=True)
    object_id = fields.Raw(required=True)
    object_data = fields.Raw(required=True)


class GetHistoryRequestSchema(Schema):
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)


class GetHistoryResponseSchema(Schema):
    history = fields.Nested(EventSchema, required=True, many=True)


def history_array_to_response(
    db_history_array: List[History], user_dict: Dict[str, User]
) -> GetHistoryResponseSchema:
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
            for row in db_history_array
        ]
    }


def get_history(request: GetHistoryRequestSchema) -> GetHistoryResponseSchema:
    history = get_db_history(request["start_date"], request["end_date"])
    user_ids = list(set([event.user_id for event in history]))
    users = get_users_by_id(user_ids)
    user_dict = {user.id: user for user in users}
    return history_array_to_response(history, user_dict)
