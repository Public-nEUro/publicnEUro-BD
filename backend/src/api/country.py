from uuid import uuid4
from flask_marshmallow import Schema
from marshmallow import fields
from .common_schemas import EmptySchema
from ..database.country import get_db_countries, GeoLocation, Country
from ..database.db_util import add_row


class CountryWithoutIdSchema(Schema):
    name = fields.String(required=True)
    geo_location = fields.Enum(GeoLocation, by_value=True, required=True)


class CountrySchema(CountryWithoutIdSchema):
    id = fields.UUID(required=True)


def db_countries_to_response(countries):
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


def add_country(request: CountryWithoutIdSchema) -> EmptySchema:
    country = Country()
    country.id = uuid4()
    country.name = request["name"]
    country.geo_location = request["geo_location"]
    add_row(country)


class GetCountriesResponseSchema(Schema):
    countries = fields.Nested(CountrySchema, required=True, many=True)


def get_countries(request: EmptySchema) -> GetCountriesResponseSchema:
    return db_countries_to_response(get_db_countries())
