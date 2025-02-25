from typing import List
from uuid import uuid4
from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import EmptySchema, IdSchema
from ..datetime import get_now
from ..database.scc import get_db_sccs, get_db_scc, Scc
from ..database.db_util import add_row


class SccSchema(Schema):
    title = fields.String(required=True)
    file_name = fields.String(required=True)


class SccWithIdSchema(SccSchema):
    id = fields.UUID(required=True)


class SccWithFileDataSchema(SccSchema):
    file_data = fields.String(required=True)


def add_scc(request: SccWithFileDataSchema) -> EmptySchema:
    scc = Scc()
    scc.id = uuid4()
    scc.title = request["title"]
    scc.file_name = request["file_name"]
    scc.file_data = request["file_data"]
    scc.timestamp = get_now()
    add_row(scc)


class GetSccResponseSchema(Schema):
    sccs = fields.Nested(SccWithIdSchema, required=True, many=True)


def db_sccs_to_response(sccs: List[Scc]) -> GetSccResponseSchema:
    return {
        "sccs": [
            {
                "id": scc.id,
                "title": scc.title,
                "file_name": scc.file_name,
                "timestamp": scc.timestamp,
            }
            for scc in sccs
        ]
    }


def get_sccs(request: EmptySchema) -> GetSccResponseSchema:
    return db_sccs_to_response(get_db_sccs())


def get_scc(request: IdSchema) -> SccWithFileDataSchema:
    scc = get_db_scc(request["id"])
    return {
        "title": scc.title,
        "file_name": scc.file_name,
        "file_data": scc.file_data,
        "timestamp": scc.timestamp,
    }
