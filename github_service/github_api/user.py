from github import PaginatedList
from github.NamedUser import NamedUser
from github.GitAuthor import GitAuthor
from github.AuthenticatedUser import AuthenticatedUser
from typing import List, Optional, Union, Dict
from .handlers.user_handler import UserHandler


class GHUser:
    def __init__(self, user: Union[NamedUser, AuthenticatedUser, Dict]) -> None:
        if user is None:
            print("User is None")
            self.login = None
            self.name = None
            self.company = None
            self.location = None
            self.email = None
            self.created_at = None
            self.type = None
        elif isinstance(user, Dict):
            self.login = user["login"]
            self.name = user["name"] if "name" in user else None
            self.company = user["company"] if "company" in user else None
            self.location = user["location"] if "location" in user else None
            self.email = user["email"] if "email" in user else None
            self.created_at = user["created_at"] if "created_at" in user else None
            self.type = user["type"] if "type" in user else None
        else:
            self.login = user.login
            self.name = user.name
            self.company = user.company
            self.location = user.location
            self.email = user.email
            self.created_at = user.created_at
            self.type = user.type

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

    def get_author_data(self, user: GitAuthor):
        named_user = UserHandler().get_user(user.name)
