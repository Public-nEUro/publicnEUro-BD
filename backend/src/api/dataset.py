from typing import List, Union
from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import EmptySchema, IdSchema, FileSchema
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


class DatasetSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    accessibility = fields.Enum(Accessibility, by_value=True, required=True)
    dua_file_name = fields.String(required=True, allow_none=True)
    dua_approval_type = fields.Enum(ApprovalType, by_value=True, required=True)
    scc_id = fields.UUID(required=True, allow_none=True)
    scc_approval_type = fields.Enum(ApprovalType, by_value=True, required=True)


class DatasetDetailsSchema(DatasetSchema):
    scc_file_name = fields.String(required=True, allow_none=True)


class DatasetWithFileDataSchema(DatasetSchema):
    dua_file_data = fields.String(required=True, allow_none=True)


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
        db_dataset.dua_approval_type = "OVERSIGHT"
        db_dataset.scc_id = None
        db_dataset.scc_approval_type = "OVERSIGHT"
        add_row(db_dataset)

    return {
        **json_dataset,
        "accessibility": db_dataset.accessibility,
        "dua_file_name": db_dataset.dua_file_name,
        "dua_approval_type": db_dataset.dua_approval_type,
        "scc_id": db_dataset.scc_id,
        "scc_approval_type": db_dataset.scc_approval_type,
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
    json_dataset = get_json_dataset(request["id"])
    db_dataset = get_db_dataset(request["id"])
    scc = get_db_scc(str(db_dataset.scc_id))
    return {
        **merge_dataset_info(json_dataset, db_dataset),
        "scc_file_name": scc.file_name if scc is not None else None,
    }


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
    dataset.dua_approval_type = request["dua_approval_type"]
    dataset.scc_id = request["scc_id"]
    dataset.scc_approval_type = request["scc_approval_type"]
    save_row(dataset)
