from flask_marshmallow import Schema
from marshmallow import fields
from ..database.user import get_user
from ..database.user_dataset import (
    get_db_user_dataset,
    get_db_user_datasets,
    UserDataset,
)


class GetUserDatasetRequestSchema(Schema):
    user_id = fields.UUID(required=True)
    dataset_id = fields.String(required=True)


class UserDatasetSchema(Schema):
    user_id = fields.UUID(required=True)
    user_email = fields.String(required=True)
    dataset_id = fields.String(required=True)
    access_requested_at = fields.DateTime(required=True, allow_none=True)
    user_accepted_dua_at = fields.DateTime(required=True, allow_none=True)
    access_granted_by_admin_at = fields.DateTime(required=True, allow_none=True)


def user_dataset_to_response(
    db_user_dataset: UserDataset,
) -> UserDatasetSchema:
    user = get_user(db_user_dataset.user_id)

    return {
        "user_id": db_user_dataset.user_id,
        "user_email": user.email,
        "dataset_id": db_user_dataset.dataset_id,
        "access_requested_at": db_user_dataset.access_requested_at,
        "user_accepted_dua_at": db_user_dataset.user_accepted_dua_at,
        "access_granted_by_admin_at": db_user_dataset.access_granted_by_admin_at,
    }


def get_user_dataset(
    request: GetUserDatasetRequestSchema,
) -> UserDatasetSchema:
    db_user_dataset = get_db_user_dataset(request["user_id"], request["dataset_id"])

    if db_user_dataset is None:
        return {
            "user_id": request["user_id"],
            "dataset_id": request["dataset_id"],
            "access_requested_at": None,
            "user_accepted_dua_at": None,
            "access_granted_by_admin_at": None,
        }

    return user_dataset_to_response(db_user_dataset)


class GetUserDatasetsRequestSchema(Schema):
    offset = fields.Integer(required=True)
    limit = fields.Integer(required=True)


class GetUserDatasetsResponseSchema(Schema):
    user_datasets = fields.Nested(UserDatasetSchema, many=True, required=True)


def get_user_datasets(
    request: GetUserDatasetsRequestSchema,
) -> GetUserDatasetsResponseSchema:
    db_user_datasets = get_db_user_datasets(request["offset"], request["limit"])
    return {
        "user_datasets": [
            user_dataset_to_response(db_user_dataset)
            for db_user_dataset in db_user_datasets
        ]
    }
