from typing import Tuple, Union
from .database.dataset import get_db_dataset, Accessibility, ApprovalType
from .database.user import get_user
from .database.institution import get_db_institution
from .database.institution_scc import get_db_institution_sccs
from .database.country import get_db_country, GeoLocation
from .geo_location import is_accessible_in_geo_location


def is_allowed_to_access_data(
    user_id: str, dataset_id: str
) -> Tuple[bool, Union[str, None]]:
    db_dataset = get_db_dataset(dataset_id)
    if db_dataset.accessibility == Accessibility.PUBLIC:
        return True, None

    user = get_user(user_id)
    if user is None:
        return False, "User not found"

    if user.email_confirmed_at is None:
        return False, "Email is not confirmed"

    if user.approved_at is None:
        return False, "User has not been approved"

    institution = get_db_institution(user.institution_id)
    if institution is None:
        return False, "Institution not found"

    if institution.country_id is None:
        return False, "Institution does not have a country"

    country = get_db_country(institution.country_id)
    if country is None:
        return False, "Country not found"

    if country.geo_location is None:
        return False, "Country has no geolocation"

    if not is_accessible_in_geo_location(
        db_dataset.accessibility, country.geo_location
    ):
        return False, "Dataset is not accessible in geolocation"

    institution_sccs = get_db_institution_sccs(institution.id)
    scc_id = str(db_dataset.scc_id)
    institution_scc = next(
        (scc for scc in institution_sccs if scc.scc_id == scc_id), None
    )

    if db_dataset.approval_type == ApprovalType.OVERSIGHT:
        return False, "Approval type is OVERSIGHT"

    if country.geo_location != GeoLocation.OTHER:
        return True, None

    if institution_scc is None:
        return False, "Institution has not accepted the SCC"

    if institution_scc.accepted is False:
        return False, "Institution has rejected the SCC"

    return True, None
