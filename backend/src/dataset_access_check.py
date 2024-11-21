import enum
from typing import Tuple, Union, Dict
from flask import current_app
from requests import HTTPError
from .database.db_util import save_row
from .database.dataset import get_db_dataset, Accessibility, ApprovalType
from .database.user import get_user
from .database.user_dataset import get_db_user_dataset, UserDataset
from .database.institution import get_db_institution
from .database.institution_scc import get_db_institution_sccs
from .database.country import get_db_country, GeoLocation
from .geo_location import is_accessible_in_geo_location
from .delphi_share import create_delphi_share
from .datetime import get_now


class AccessRequestStatus(enum.Enum):
    USER_NOT_FOUND = "USER_NOT_FOUND"
    EMAIL_NOT_CONFIRMED = "EMAIL_NOT_CONFIRMED"
    USER_NOT_APPROVED = "USER_NOT_APPROVED"
    INSTITUTION_NOT_FOUND = "INSTITUTION_NOT_FOUND"
    INSTITUTION_HAS_NO_COUNTRY = "INSTITUTION_HAS_NO_COUNTRY"
    COUNTRY_NOT_FOUND = "COUNTRY_NOT_FOUND"
    COUNTRY_HAS_NO_GEOLOCATION = "COUNTRY_HAS_NO_GEOLOCATION"
    NOT_ACCESSIBLE_IN_GEOLOCATION = "NOT_ACCESSIBLE_IN_GEOLOCATION"
    NEEDS_ADMIN_APPROVAL = "NEEDS_ADMIN_APPROVAL"
    INSTITUTION_HAS_NOT_ACCEPTED_SCC = "INSTITUTION_HAS_NOT_ACCEPTED_SCC"
    INSTITUTION_HAS_REJECTED_SCC = "INSTITUTION_HAS_REJECTED_SCC"
    ACCESSIBLE = "ACCESSIBLE"


access_request_status_to_message: Dict[AccessRequestStatus, str] = {
    AccessRequestStatus.USER_NOT_FOUND: "User not found",
    AccessRequestStatus.EMAIL_NOT_CONFIRMED: "Email is not confirmed",
    AccessRequestStatus.USER_NOT_APPROVED: "User has not been approved",
    AccessRequestStatus.INSTITUTION_NOT_FOUND: "Institution not found",
    AccessRequestStatus.INSTITUTION_HAS_NO_COUNTRY: "Institution does not have a country",
    AccessRequestStatus.COUNTRY_NOT_FOUND: "Country not found",
    AccessRequestStatus.COUNTRY_HAS_NO_GEOLOCATION: "Country has no geolocation",
    AccessRequestStatus.NOT_ACCESSIBLE_IN_GEOLOCATION: "Dataset is not accessible in geolocation",
    AccessRequestStatus.NEEDS_ADMIN_APPROVAL: "Approval type is OVERSIGHT. Admin needs to approve.",
    AccessRequestStatus.INSTITUTION_HAS_NOT_ACCEPTED_SCC: "Institution has not accepted the SCC",
    AccessRequestStatus.INSTITUTION_HAS_REJECTED_SCC: "Institution has rejected the SCC",
    AccessRequestStatus.ACCESSIBLE: "You will receive an email with a download link.",
}


access_request_status_to_admin_message: Dict[AccessRequestStatus, str] = {
    AccessRequestStatus.USER_NOT_FOUND: "User not found",
    AccessRequestStatus.EMAIL_NOT_CONFIRMED: "Email is not confirmed",
    AccessRequestStatus.USER_NOT_APPROVED: "User has not been approved",
    AccessRequestStatus.INSTITUTION_NOT_FOUND: "Institution not found",
    AccessRequestStatus.INSTITUTION_HAS_NO_COUNTRY: "Institution does not have a country",
    AccessRequestStatus.COUNTRY_NOT_FOUND: "Country not found",
    AccessRequestStatus.COUNTRY_HAS_NO_GEOLOCATION: "Country has no geolocation",
    AccessRequestStatus.NOT_ACCESSIBLE_IN_GEOLOCATION: "Dataset is not accessible in geolocation",
    AccessRequestStatus.NEEDS_ADMIN_APPROVAL: "Approval type is OVERSIGHT. The request needs approval.",
    AccessRequestStatus.INSTITUTION_HAS_NOT_ACCEPTED_SCC: "Institution has not accepted the SCC",
    AccessRequestStatus.INSTITUTION_HAS_REJECTED_SCC: "Institution has rejected the SCC",
    AccessRequestStatus.ACCESSIBLE: "The user has received an email with a download link.",
}


def get_access_request_status(user_id: str, dataset_id: str) -> Accessibility:
    db_dataset = get_db_dataset(dataset_id)
    if db_dataset.accessibility == Accessibility.PUBLIC:
        return AccessRequestStatus.ACCESSIBLE

    user = get_user(user_id)
    if user is None:
        return AccessRequestStatus.USER_NOT_FOUND

    if user.email_confirmed_at is None:
        return AccessRequestStatus.EMAIL_NOT_CONFIRMED

    if user.approved_at is None:
        return AccessRequestStatus.USER_NOT_APPROVED

    institution = get_db_institution(user.institution_id)
    if institution is None:
        return AccessRequestStatus.INSTITUTION_NOT_FOUND

    if institution.country_id is None:
        return AccessRequestStatus.INSTITUTION_HAS_NO_COUNTRY

    country = get_db_country(institution.country_id)
    if country is None:
        return AccessRequestStatus.COUNTRY_NOT_FOUND

    if country.geo_location is None:
        return AccessRequestStatus.COUNTRY_HAS_NO_GEOLOCATION

    if not is_accessible_in_geo_location(
        db_dataset.accessibility, country.geo_location
    ):
        return AccessRequestStatus.NOT_ACCESSIBLE_IN_GEOLOCATION

    institution_sccs = get_db_institution_sccs(institution.id)
    scc_id = str(db_dataset.scc_id)
    institution_scc = next(
        (scc for scc in institution_sccs if scc.scc_id == scc_id), None
    )

    if db_dataset.approval_type == ApprovalType.OVERSIGHT:
        db_user_dataset = get_db_user_dataset(user_id, dataset_id)
        if (
            db_user_dataset is None
            or db_user_dataset.access_granted_by_admin_at is None
        ):
            return AccessRequestStatus.NEEDS_ADMIN_APPROVAL

    if country.geo_location != GeoLocation.OTHER:
        return AccessRequestStatus.ACCESSIBLE

    if institution_scc is None:
        return AccessRequestStatus.INSTITUTION_HAS_NOT_ACCEPTED_SCC

    if institution_scc.accepted is False:
        return AccessRequestStatus.INSTITUTION_HAS_REJECTED_SCC

    return AccessRequestStatus.ACCESSIBLE


def set_delphi_share_created(user_dataset: UserDataset) -> None:
    user_dataset.delphi_share_created_at = get_now()
    save_row(user_dataset)


def perform_access_check(
    user_id: str, dataset_id: str, is_allowed_access: bool, reason: str
) -> str:
    if not is_allowed_access:
        return (
            f"Your access request has been received. Further action is needed: {reason}"
        )

    user_dataset = get_db_user_dataset(user_id, dataset_id)

    already_received_message = "You already received an email with a download link."

    if user_dataset.delphi_share_created_at is not None:
        return already_received_message

    user = get_user(user_id)
    dataset = get_db_dataset(dataset_id)

    try:
        create_delphi_share(dataset.delphi_share_url, user.email)
    except HTTPError as e:
        if e.response.status_code == 409:
            set_delphi_share_created(user_dataset)
            return already_received_message
        current_app.logger.exception(str(e))
        return "An error occurred."

    set_delphi_share_created(user_dataset)

    return "You will receive an email with a download link."
