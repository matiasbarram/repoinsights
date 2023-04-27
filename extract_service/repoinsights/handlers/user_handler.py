from github import Github
from ...config import GHToken


class InsightsUserHandler:
    def __init__(self) -> None:
        self.token = GHToken().get_token()
        self.gh = Github(self.token, per_page=100)

    def get_user(self, username: str):
        return self.gh.get_user(username)
