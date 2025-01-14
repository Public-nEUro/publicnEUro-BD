from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from ..database.user_dataset import get_db_user_dataset
from ..database.db_util import delete_row
from .common_schemas import EmptySchema


class DeleteAccessRequestRequestSchema(Schema):
    user_id = fields.String(required=True)
    dataset_id = fields.String(required=True)


def delete_access_request(request: DeleteAccessRequestRequestSchema) -> EmptySchema:
    db_user_dataset = get_db_user_dataset(request["user_id"], request["dataset_id"])

    if db_user_dataset is None:
        abort(404)

    delete_row(db_user_dataset)

    return {}
