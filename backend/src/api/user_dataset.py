from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from ..database.user import get_user
from ..database.user_dataset import (
    get_db_user_dataset,
    get_db_user_datasets,
    get_db_user_datasets_count,
    get_db_user_datasets_for_dataset,
    UserDataset,
)
from .common_schemas import PaginationSchema
from .assertions import get_logged_in_user_or_abort


class GetUserDatasetRequestSchema(Schema):
    user_id = fields.UUID(required=True)
    dataset_id = fields.String(required=True)


class UserDatasetSchema(Schema):
    user_id = fields.UUID(required=True)
    user_email = fields.String(required=True)
    dataset_id = fields.String(required=True)
    access_requested_at = fields.DateTime(required=True, allow_none=True)
    user_accepted_dua_at = fields.DateTime(required=True, allow_none=True)
    signed_dua_file_name = fields.String(required=True, allow_none=True)
    signed_dua_file_data = fields.String(required=True, allow_none=True)
    email_sent_to_admin_at = fields.DateTime(required=True, allow_none=True)
    access_granted_by_admin_at = fields.DateTime(required=True, allow_none=True)
    delphi_share_created_at = fields.DateTime(required=True, allow_none=True)


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
        "signed_dua_file_name": db_user_dataset.signed_dua_file_name,
        "signed_dua_file_data": db_user_dataset.signed_dua_file_data,
        "email_sent_to_admin_at": db_user_dataset.email_sent_to_admin_at,
        "access_granted_by_admin_at": db_user_dataset.access_granted_by_admin_at,
        "delphi_share_created_at": db_user_dataset.delphi_share_created_at,
    }


def get_user_dataset(
    request: GetUserDatasetRequestSchema,
) -> UserDatasetSchema:
    user = get_logged_in_user_or_abort()

    if not user.is_admin and user.id != request["user_id"]:
        abort(403)

    db_user_dataset = get_db_user_dataset(request["user_id"], request["dataset_id"])

    if db_user_dataset is None:
        return {
            "user_id": request["user_id"],
            "dataset_id": request["dataset_id"],
            "access_requested_at": None,
            "user_accepted_dua_at": None,
            "email_sent_to_admin_at": None,
            "access_granted_by_admin_at": None,
            "delphi_share_created_at": None,
        }

    return user_dataset_to_response(db_user_dataset)


class GetUserDatasetsResponseSchema(Schema):
    user_datasets = fields.Nested(UserDatasetSchema, many=True, required=True)
    total = fields.Integer(required=True)


def get_user_datasets(
    request: PaginationSchema,
) -> GetUserDatasetsResponseSchema:
    db_user_datasets = get_db_user_datasets(request["offset"], request["limit"])
    return {
        "user_datasets": [
            user_dataset_to_response(db_user_dataset)
            for db_user_dataset in db_user_datasets
        ],
        "total": get_db_user_datasets_count(),
    }


class GetUserDatasetsForDatasetRequestSchema(Schema):
    dataset_id = fields.String(required=True)


class GetUserDatasetsForDatasetResponseSchema(Schema):
    user_datasets = fields.Nested(UserDatasetSchema, many=True, required=True)


def get_user_datasets_for_dataset(
    request: GetUserDatasetsForDatasetRequestSchema,
) -> GetUserDatasetsForDatasetResponseSchema:
    db_user_datasets = get_db_user_datasets_for_dataset(request["dataset_id"])
    return {
        "user_datasets": [
            user_dataset_to_response(db_user_dataset)
            for db_user_dataset in db_user_datasets
        ]
    }
