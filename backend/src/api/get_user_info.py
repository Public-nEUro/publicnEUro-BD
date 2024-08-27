from .common_schemas import EmptySchema, UserInfo, extract_user_info
from .assertions import get_logged_in_user_or_abort


def get_user_info(request: EmptySchema) -> UserInfo:
    user = get_logged_in_user_or_abort()

    return extract_user_info(user)
