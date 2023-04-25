from datetime import datetime, timedelta
from typing import Union, List, Dict, Set


def format_dt(dt: datetime) -> str:
    return dt.strftime("%B %d, %Y, %I:%M %p")


def gh_api_to_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")


def get_user_type(type) -> Union[str, None]:
    if type == "Organization":
        return "ORG"
    elif type == "User":
        return "USR"
    elif type == "Bot":
        return "BOT"
    else:
        return None


def get_first_last_days_month(month: datetime):
    first_day = month.replace(day=1)
    if month.month != 12:
        last_day = month.replace(
            day=month.day,
            month=month.month + 1,
        ) - timedelta(days=1)
    else:
        last_day = month.replace(
            day=1,
            month=1,
            year=month.year + 1,
        ) - timedelta(days=1)
    return first_day, last_day


def get_n_months(start_date: datetime, end_date: datetime):
    months = (
        (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1
    )
    return months


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def compare_dates(date1, date2):
    date1 = datetime.strptime(date1, "%Y-%m-%d")
    date2 = datetime.strptime(date2, "%Y-%m-%d")
    return (date1 > date2) - (date1 < date2)


def add_users_to_dict_keys(list_dicts: List, users: Dict, user_keys: List[str]):
    for dict in list_dicts:
        for key in user_keys:
            keys = key.split(".")
            user_obj = dict
            for k in keys[:-1]:
                if user_obj is not None:
                    user_obj = user_obj.get(k)
                else:
                    break
            if user_obj is not None:
                last_key = keys[-1]
                if user_obj[last_key] is not None:
                    user_obj[last_key] = users[user_obj[last_key]["login"]]


def get_unique_users(elements, user_key: str) -> Set[str]:
    users_to_fetch = set()
    for element in elements:
        keys = user_key.split(".")
        user_obj = element
        for key in keys:
            if user_obj is not None:
                user_obj = user_obj.get(key)
            else:
                break
        if user_obj is not None:
            users_to_fetch.add(user_obj["login"])
    return users_to_fetch
