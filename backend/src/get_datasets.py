from typing import List, Union
import re
import hashlib
import requests
from flask_marshmallow import Schema
from marshmallow import fields


def get_datasets_url():
    json = requests.get("http://datalad:3000/metadata/super.json").json()
    dataset_id = json["dataset_id"]
    dataset_version = json["dataset_version"]
    md5 = hashlib.md5(f"{dataset_id}-{dataset_version}".encode("utf-8")).hexdigest()
    folder_name = md5[:3]
    file_name = md5[3:]
    return f"http://datalad:3000/metadata/{dataset_id}/{dataset_version}/{folder_name}/{file_name}.json"


def convert_dataset(dataset):
    name = dataset["dataset_id"]
    id = re.split(r"\W+", name)[0]
    return {
        "id": id,
        "name": name,
    }


class JsonDataset(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)


def get_json_datasets() -> List[JsonDataset]:
    url = get_datasets_url()
    json = requests.get(url).json()
    datasets = json["subdatasets"]
    return [convert_dataset(dataset) for dataset in datasets]


def get_json_dataset(id: str) -> Union[JsonDataset, None]:
    return next(
        (
            json_dataset
            for json_dataset in get_json_datasets()
            if json_dataset["id"] == id
        ),
        None,
    )
