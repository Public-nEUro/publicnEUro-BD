from typing import List
from uuid import uuid4
from flask import abort
from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import EmptySchema, IdSchema
from ..database.country import get_db_country, get_db_countries, GeoLocation, Country
from ..database.db_util import add_row, delete_row


class CountryWithoutIdSchema(Schema):
    name = fields.String(required=True)
    geo_location = fields.Enum(GeoLocation, by_value=True, required=True)


class CountrySchema(CountryWithoutIdSchema):
    id = fields.UUID(required=True)


def add_country(request: CountryWithoutIdSchema) -> EmptySchema:
    country = Country()
    country.id = uuid4()
    country.name = request["name"]
    country.geo_location = request["geo_location"]
    add_row(country)


def delete_country(request: IdSchema) -> EmptySchema:
    country = get_db_country(request["id"])
    if country is None:
        abort(404)

    delete_row(country)


class GetCountriesResponseSchema(Schema):
    countries = fields.Nested(CountrySchema, required=True, many=True)


def db_countries_to_response(countries: List[Country]) -> GetCountriesResponseSchema:
    return {
        "countries": [
            {
                "id": country.id,
                "name": country.name,
                "geo_location": country.geo_location,
            }
            for country in countries
        ]
    }


def get_countries(request: EmptySchema) -> GetCountriesResponseSchema:
    return db_countries_to_response(get_db_countries())
