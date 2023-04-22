from typing import List, Optional, Union, Dict
from github.NamedUser import NamedUser
from github.GitAuthor import GitAuthor
from .handlers.user_handler import UserHandler
from ..utils.utils import get_user_type


class GHUser:
    def __init__(self, user: Union[NamedUser, Dict]) -> None:
        if isinstance(user, Dict):
            self._set_attributes_from_dict(user)
        else:
            self._set_attributes_from_object(user)

    def _set_attributes_from_dict(self, user: Dict) -> None:
        self.login = user.get("login")
        self.name = user.get("name")
        self.company = user.get("company")
        self.location = user.get("location")
        self.email = user.get("email")
        self.created_at = user.get("created_at")
        self.type = get_user_type(user.get("type"))

    def _set_attributes_from_object(self, user: NamedUser) -> None:
        self.login = user.login
        self.name = user.name
        self.company = user.company
        self.location = user.location
        self.email = user.email
        self.created_at = user.created_at
        self.type = get_user_type(user.type)

    def to_dict(self) -> dict:
        return {
            "login": self.login,
            "name": self.name,
            "company": self.company,
            "location": self.location,
            "email": self.email,
            "created_at": self.created_at,
            "type": self.type,
        }
