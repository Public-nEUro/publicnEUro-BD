from typing import List
from flask_marshmallow import Schema
from marshmallow import fields
from ..database.history import History, get_db_history


class EventSchema(Schema):
    id = fields.String(required=True)
    timestamp = fields.DateTime(required=True)
    user_id = fields.String(required=True)
    object_id = fields.String(required=True)
    object_data = fields.String(required=True)


class GetHistoryRequestSchema(Schema):
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)


class GetHistoryResponseSchema(Schema):
    history = fields.Nested(EventSchema, required=True, many=True)


def history_array_to_response(
    db_history_array: List[History],
) -> GetHistoryResponseSchema:
    return {
        "history": [
            {
                "id": row.id,
                "timestamp": row.timestamp,
                "user_id": row.user_id,
                "object_id": row.object_id,
                "object_data": row.object_data,
            }
            for row in db_history_array
        ]
    }


def get_history(request: GetHistoryRequestSchema) -> GetHistoryResponseSchema:
    return history_array_to_response(
        get_db_history(request["start_date"], request["end_date"])
    )
