from datetime import datetime
from typing import Union


def format_dt(dt: datetime) -> str:
    return dt.strftime("%B %d, %Y, %I:%M %p")


def get_user_type(type) -> Union[str, None]:
    if type == "Organization":
        return "ORG"
    if type == "User":
        return "USR"
    else:
        return None
