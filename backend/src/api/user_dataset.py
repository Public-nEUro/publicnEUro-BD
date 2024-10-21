from flask_marshmallow import Schema
from marshmallow import fields
from ..database.user_dataset import get_db_user_dataset, UserDataset


class GetUserDatasetRequestSchema(Schema):
    user_id = fields.UUID(required=True)
    dataset_id = fields.String(required=True)


class GetUserDatasetResponseSchema(Schema):
    user_id = fields.UUID(required=True)
    dataset_id = fields.String(required=True)
    access_requested_at = fields.DateTime(required=True, allow_none=True)
    dua_accepted_at = fields.DateTime(required=True, allow_none=True)
    scc_accepted_at = fields.DateTime(required=True, allow_none=True)
    access_granted_by_admin_at = fields.DateTime(required=True, allow_none=True)


def user_dataset_to_response(
    db_user_dataset: UserDataset,
) -> GetUserDatasetResponseSchema:
    return {
        "user_id": db_user_dataset.user_id,
        "dataset_id": db_user_dataset.dataset_id,
        "access_requested_at": db_user_dataset.access_requested_at,
        "dua_accepted_at": db_user_dataset.dua_accepted_at,
        "scc_accepted_at": db_user_dataset.scc_accepted_at,
        "access_granted_by_admin_at": db_user_dataset.access_granted_by_admin_at,
    }


def get_user_dataset(
    request: GetUserDatasetRequestSchema,
) -> GetUserDatasetResponseSchema:
    db_user_dataset = get_db_user_dataset(request["user_id"], request["dataset_id"])

    if db_user_dataset is None:
        return {
            "user_id": request["user_id"],
            "dataset_id": request["dataset_id"],
            "access_requested_at": None,
            "dua_accepted_at": None,
            "scc_accepted_at": None,
            "access_granted_by_admin_at": None,
        }

    return user_dataset_to_response(db_user_dataset)
