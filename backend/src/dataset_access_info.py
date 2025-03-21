from flask_marshmallow import Schema
from marshmallow import fields
from .database.dataset import get_db_dataset, Accessibility
from .database.user import get_user
from .database.institution import get_db_institution
from .database.institution_scc import get_db_institution_sccs
from .database.country import get_db_country, GeoLocation
from .geo_location import is_accessible_in_geo_location


class AccessInfo(Schema):
    needs_to_log_in = fields.Boolean(required=True)
    needs_to_confirm_email = fields.Boolean(required=True)
    needs_to_be_approved = fields.Boolean(required=True)
    is_scc_relevant = fields.Boolean(required=True)
    has_rejected_scc = fields.Boolean(required=True)
    user_has_country = fields.Boolean(required=True)
    is_accessible_in_country = fields.Boolean(required=True)


def get_access_info(user_id: str, dataset_id: str) -> AccessInfo:
    user = get_user(user_id)
    institution = get_db_institution(user.institution_id) if user is not None else None
    country = (
        get_db_country(institution.country_id)
        if institution is not None and institution.country_id is not None
        else None
    )
    institution_sccs = (
        get_db_institution_sccs(institution.id) if institution is not None else []
    )
    db_dataset = get_db_dataset(dataset_id)
    scc_id = str(db_dataset.scc_id)
    institution_scc = next(
        (scc for scc in institution_sccs if scc.scc_id == scc_id), None
    )
    not_public = db_dataset.accessibility != Accessibility.OPEN

    return {
        "needs_to_log_in": not_public and user is None,
        "needs_to_confirm_email": not_public
        and user is not None
        and user.email_confirmed_at is None,
        "needs_to_be_approved": not_public
        and user is not None
        and user.approved_at is None,
        "is_scc_relevant": not_public
        and country is not None
        and country.geo_location == GeoLocation.OTHER,
        "has_rejected_scc": institution_scc is not None
        and institution_scc.accepted is False,
        "user_has_country": country is not None,
        "is_accessible_in_country": is_accessible_in_geo_location(
            db_dataset.accessibility,
            country.geo_location if country is not None else None,
        ),
    }
