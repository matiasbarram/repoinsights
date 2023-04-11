from github import Github
from config import GHGetToken


class UserHandler:
    def __init__(self) -> None:
        self.token = GHGetToken().get_token()
        self.gh = Github(self.token, per_page=100)

    def get_user(self, username: str):
        return self.gh.get_user(username)
