from .database.dataset import Accessibility
from .database.country import GeoLocation


def is_accessible_in_geo_location(
    accessibility: Accessibility, geo_location: GeoLocation
) -> bool:
    match accessibility:
        case Accessibility.PUBLIC:
            return True
        case Accessibility.WORLDWIDE:
            return True
        case Accessibility.EU_AND_ADEQUATE:
            return geo_location in (GeoLocation.EU, GeoLocation.ADEQUATE)
        case Accessibility.EU:
            return geo_location == GeoLocation.EU
        case Accessibility.PRIVATE:
            return False
