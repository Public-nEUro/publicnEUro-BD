from typing import List
from uuid import uuid4
from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import EmptySchema
from ..database.institution import get_db_institutions, Institution, Acceptance
from ..database.db_util import add_row


class InstitutionWithoutIdSchema(Schema):
    name = fields.String(required=True)
    contact = fields.String(required=True)
    country_id = fields.UUID(required=True)
    scc_acceptance = fields.Enum(Acceptance, by_value=True, required=True)


class InstitutionSchema(InstitutionWithoutIdSchema):
    id = fields.UUID(required=True)


def db_insitutinos_to_response(countries: List[Institution]):
    return {
        "institutions": [
            {
                "id": institution.id,
                "name": institution.name,
                "contact": institution.contact,
                "country_id": institution.country_id,
                "scc_acceptance": institution.scc_acceptance,
            }
            for institution in countries
        ]
    }


def add_institution(request: InstitutionWithoutIdSchema) -> EmptySchema:
    institution = Institution()
    institution.id = uuid4()
    institution.name = request["name"]
    institution.contact = request["contact"]
    institution.country_id = request["country_id"]
    institution.scc_acceptance = request["scc_acceptance"]
    add_row(institution)


class GetInstitutionsResponseSchema(Schema):
    institutions = fields.Nested(InstitutionSchema, required=True, many=True)


def get_institutions(request: EmptySchema) -> GetInstitutionsResponseSchema:
    return db_insitutinos_to_response(get_db_institutions())
