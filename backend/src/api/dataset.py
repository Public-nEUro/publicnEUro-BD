from typing import List, Union
from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import EmptySchema, IdSchema, FileSchema
from .assertions import get_logged_in_admin_or_abort
from ..auth.token import get_auth_user_id
from ..database.user import get_user
from ..database.institution import get_db_institution
from ..database.institution_scc import get_db_institution_sccs
from ..database.dataset import (
    get_db_datasets,
    get_db_dataset,
    Dataset,
    Accessibility,
    ApprovalType,
)
from ..get_datasets import get_json_datasets, get_json_dataset, JsonDataset
from ..database.db_util import add_row, save_row
from ..database.scc import get_db_scc
from ..dataset_access_info import AccessInfo, get_access_info


class DatasetSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    accessibility = fields.Enum(Accessibility, by_value=True, required=True)
    dua_file_name = fields.String(required=True, allow_none=True)
    scc_id = fields.UUID(required=True, allow_none=True)
    approval_type = fields.Enum(ApprovalType, by_value=True, required=True)


class DatasetWithFileDataSchema(DatasetSchema):
    dua_file_data = fields.String(required=True, allow_none=True)
    delphi_share_url = fields.String(required=True)


class DatasetDetailsSchema(DatasetSchema):
    dua_file_data = fields.String(required=True, allow_none=True)
    scc_file_name = fields.String(required=True, allow_none=True)
    institution_scc_accepted = fields.Boolean(required=True, allow_none=True)
    access_info = fields.Nested(AccessInfo, required=True)


class DelphiShareUrlSchema(Schema):
    delphi_share_url = fields.String(required=True)


class GetDatasetsResponseSchema(Schema):
    datasets = fields.Nested(DatasetSchema, required=True, many=True)


def merge_dataset_info(
    json_dataset: JsonDataset, db_dataset: Union[Dataset, None]
) -> DatasetSchema:
    if db_dataset is None:
        db_dataset = Dataset()
        db_dataset.id = json_dataset["id"]
        db_dataset.accessibility = "PRIVATE"
        db_dataset.dua_file_name = None
        db_dataset.dua_file_data = None
        db_dataset.scc_id = None
        db_dataset.approval_type = "OVERSIGHT"
        db_dataset.delphi_share_url = ""
        add_row(db_dataset)

    return {
        **json_dataset,
        "accessibility": db_dataset.accessibility,
        "dua_file_name": db_dataset.dua_file_name,
        "scc_id": db_dataset.scc_id,
        "approval_type": db_dataset.approval_type,
    }


def datasets_to_response(
    json_datasets: List[JsonDataset], db_datasets: List[Dataset]
) -> GetDatasetsResponseSchema:
    db_datasets_dict = {dataset.id: dataset for dataset in db_datasets}

    return {
        "datasets": [
            merge_dataset_info(
                json_dataset, db_datasets_dict.get(json_dataset["id"], None)
            )
            for json_dataset in json_datasets
        ]
    }


def get_datasets(request: EmptySchema) -> GetDatasetsResponseSchema:
    json_datasets = get_json_datasets()
    db_datasets = get_db_datasets()
    return datasets_to_response(json_datasets, db_datasets)


def get_dataset(request: IdSchema) -> DatasetDetailsSchema:
    user_id = get_auth_user_id()
    user = get_user(user_id)
    institution = get_db_institution(user.institution_id) if user is not None else None
    institution_sccs = (
        get_db_institution_sccs(institution.id) if institution is not None else []
    )
    json_dataset = get_json_dataset(request["id"])
    db_dataset = get_db_dataset(request["id"])
    dataset_info = merge_dataset_info(json_dataset, db_dataset)
    scc_id = dataset_info["scc_id"]
    institution_scc = next(
        (scc for scc in institution_sccs if scc.scc_id == scc_id), None
    )
    scc = get_db_scc(scc_id)
    return {
        **dataset_info,
        "dua_file_data": db_dataset.dua_file_data,
        "scc_file_name": scc.file_name if scc is not None else None,
        "institution_scc_accepted": (
            institution_scc.accepted if institution_scc is not None else None
        ),
        "access_info": get_access_info(user_id, request["id"]),
    }


def get_delphi_share_url(request: IdSchema) -> DelphiShareUrlSchema:
    db_dataset = get_db_dataset(request["id"])

    if db_dataset is None:
        abort(404)

    if db_dataset.accessibility != Accessibility.OPEN:
        get_logged_in_admin_or_abort()

    return {"delphi_share_url": db_dataset.delphi_share_url}


def get_dataset_dua(request: IdSchema) -> FileSchema:
    dataset = get_db_dataset(request["id"])

    if dataset is None:
        abort(404)

    return {
        "file_name": dataset.dua_file_name,
        "file_data": dataset.dua_file_data,
    }


def update_dataset(request: DatasetWithFileDataSchema) -> EmptySchema:
    dataset = get_db_dataset(request["id"])
    dataset.accessibility = request["accessibility"]
    dataset.dua_file_name = request["dua_file_name"]
    if request["dua_file_data"] is not None:
        dataset.dua_file_data = request["dua_file_data"]
    dataset.scc_id = request["scc_id"]
    dataset.approval_type = request["approval_type"]
    dataset.delphi_share_url = request["delphi_share_url"]
    save_row(dataset)
