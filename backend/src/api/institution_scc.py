from typing import List
from flask_marshmallow import Schema
from marshmallow import fields
from ..database.institution_scc import get_db_institution_sccs, InstitutionScc


class GetInstitutionSccsRequestSchema(Schema):
    institution_id = fields.UUID(required=True)


class InstitutionSccSchema(Schema):
    scc_id = fields.UUID(required=True)
    accepted = fields.Boolean(required=True)
    timestamp = fields.DateTime(required=True)


class GetInstitutionSccsResponseSchema(Schema):
    institution_sccs = fields.Nested(InstitutionSccSchema, required=True, many=True)


def institution_sccs_to_response(
    db_institution_sccs: List[InstitutionScc],
) -> GetInstitutionSccsResponseSchema:
    return {
        "institution_sccs": [
            {
                "scc_id": db_institution_scc.scc_id,
                "accepted": db_institution_scc.accepted,
                "timestamp": db_institution_scc.timestamp,
            }
            for db_institution_scc in db_institution_sccs
        ]
    }


def get_institution_sccs(
    request: GetInstitutionSccsRequestSchema,
) -> GetInstitutionSccsResponseSchema:
    db_institution_sccs = get_db_institution_sccs(request["institution_id"])

    return institution_sccs_to_response(db_institution_sccs)
