from typing import List
from uuid import uuid4
from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import EmptySchema
from ..database.institution import get_db_institutions, get_db_institution, Institution
from ..database.scc import get_db_sccs, Scc
from ..database.institution_scc import get_db_institutions_sccs, InstitutionScc
from ..database.db_util import add_row, save_row


class InstitutionWithoutIdSchema(Schema):
    name = fields.String(required=True)
    contact = fields.String(required=True)
    country_id = fields.UUID(required=True, allow_none=True)


class InstitutionSchema(InstitutionWithoutIdSchema):
    id = fields.UUID(required=True)
    has_rejected_all_sccs = fields.Boolean(required=True)


def add_institution(request: InstitutionWithoutIdSchema) -> EmptySchema:
    institution = Institution()
    institution.id = uuid4()
    institution.name = request["name"]
    institution.contact = request["contact"]
    institution.country_id = request["country_id"]
    add_row(institution)


class GetInstitutionsResponseSchema(Schema):
    institutions = fields.Nested(InstitutionSchema, required=True, many=True)


def db_insitutions_to_response(
    db_institutions: List[Institution],
    db_sccs: List[Scc],
    db_institutions_sccs: List[InstitutionScc],
) -> GetInstitutionsResponseSchema:
    institution_scc_accepted = {
        db_institution.id: {db_scc.id: None for db_scc in db_sccs}
        for db_institution in db_institutions
    }

    for db_institution_scc in db_institutions_sccs:
        institution_scc_accepted[db_institution_scc.institution_id][
            db_institution_scc.scc_id
        ] = db_institution_scc.accepted

    return {
        "institutions": [
            {
                "id": institution.id,
                "name": institution.name,
                "contact": institution.contact,
                "country_id": institution.country_id,
                "has_rejected_all_sccs": any(
                    accepted is False
                    for accepted in institution_scc_accepted[institution.id]
                ),
            }
            for institution in db_institutions
        ]
    }


def get_institutions(request: EmptySchema) -> GetInstitutionsResponseSchema:
    return db_insitutions_to_response(
        get_db_institutions(), get_db_sccs(), get_db_institutions_sccs()
    )


def update_institution(request: InstitutionSchema) -> EmptySchema:
    institution = get_db_institution(request["id"])
    institution.name = request["name"]
    institution.contact = request["contact"]
    institution.country_id = request["country_id"]
    save_row(institution)
