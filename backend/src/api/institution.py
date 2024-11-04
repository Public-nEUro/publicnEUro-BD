from typing import List, Union
from uuid import uuid4, UUID
from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import EmptySchema
from ..database.institution import get_db_institutions, get_db_institution, Institution
from ..database.scc import get_db_sccs, Scc
from ..database.institution_scc import (
    get_db_institutions_sccs,
    get_db_institution_sccs,
    InstitutionScc,
)
from ..database.db_util import add_row, save_row, delete_row
from .institution_scc import AcceptanceSchema
from ..datetime import get_now


class InstitutionWithoutIdSchema(Schema):
    name = fields.String(required=True)
    contact = fields.String(required=True)
    country_id = fields.UUID(required=True, allow_none=True)


class InstitutionSchema(InstitutionWithoutIdSchema):
    id = fields.UUID(required=True)
    has_rejected_all_sccs = fields.Boolean(required=True)


class InstitutionWithAcceptanceSchema(InstitutionSchema):
    scc_acceptance = fields.Dict(
        fields.UUID, fields.Nested(AcceptanceSchema), required=True
    )


def add_institution(request: InstitutionWithoutIdSchema) -> EmptySchema:
    institution = Institution()
    institution.id = uuid4()
    institution.name = request["name"]
    institution.contact = request["contact"]
    institution.country_id = request["country_id"]
    add_row(institution)


class GetInstitutionsResponseSchema(Schema):
    institutions = fields.Nested(
        InstitutionWithAcceptanceSchema, required=True, many=True
    )


def db_insitutions_to_response(
    db_institutions: List[Institution],
    db_sccs: List[Scc],
    db_institutions_sccs: List[InstitutionScc],
) -> GetInstitutionsResponseSchema:
    institution_scc: dict[UUID, dict[str, Union[InstitutionScc, None]]] = {
        db_institution.id: {
            db_scc.id: {"accepted": None, "timestamp": None} for db_scc in db_sccs
        }
        for db_institution in db_institutions
    }

    for db_institution_scc in db_institutions_sccs:
        institution_scc[db_institution_scc.institution_id][
            db_institution_scc.scc_id
        ] = {
            "accepted": db_institution_scc.accepted,
            "timestamp": db_institution_scc.timestamp,
        }

    return {
        "institutions": [
            {
                "id": institution.id,
                "name": institution.name,
                "contact": institution.contact,
                "country_id": institution.country_id,
                "has_rejected_all_sccs": all(
                    institution_scc is not None and institution_scc["accepted"] is False
                    for institution_scc in institution_scc[institution.id].values()
                ),
                "scc_acceptance": {
                    scc.id: institution_scc[institution.id][scc.id] for scc in db_sccs
                },
            }
            for institution in db_institutions
        ]
    }


def get_institutions(request: EmptySchema) -> GetInstitutionsResponseSchema:
    return db_insitutions_to_response(
        get_db_institutions(), get_db_sccs(), get_db_institutions_sccs()
    )


def update_institution(request: InstitutionWithAcceptanceSchema) -> EmptySchema:
    institution = get_db_institution(request["id"])
    institution.name = request["name"]
    institution.contact = request["contact"]
    institution.country_id = request["country_id"]
    save_row(institution)

    institution_sccs = {
        institution_scc.scc_id: institution_scc
        for institution_scc in get_db_institution_sccs(request["id"])
    }

    for scc_id, scc_acceptance in request["scc_acceptance"].items():
        old_institution_scc = institution_sccs.get(str(scc_id), None)

        if old_institution_scc is not None:
            if scc_acceptance["accepted"] == old_institution_scc.accepted:
                continue

            delete_row(old_institution_scc)

        if scc_acceptance["accepted"] is None:
            continue

        institution_scc = InstitutionScc()
        institution_scc.institution_id = institution.id
        institution_scc.scc_id = scc_id
        institution_scc.accepted = scc_acceptance["accepted"]
        institution_scc.timestamp = get_now()
        add_row(institution_scc)
