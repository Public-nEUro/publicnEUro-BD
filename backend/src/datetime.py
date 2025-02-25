from datetime import datetime
import pytz


def get_now():
    return datetime.now(tz=pytz.timezone("UTC"))
