from .GHToken import GHToken
from github import Github


class GHGetToken(GHToken):
    def __init__(self) -> None:
        token_list = self.get_public_tokens(token=None)
        self.connector = self.get_github_connector(token_list)
