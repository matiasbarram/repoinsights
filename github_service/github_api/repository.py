from config import GHGetToken
from github import Repository


class GHRepository:
    def __init__(self, gh_token: GHGetToken, gh_repo: str) -> None:
        self.connector = gh_token.connector
        self.repo: Repository.Repository = self.connector.get_repo(gh_repo)
