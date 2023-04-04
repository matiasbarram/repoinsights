from .GHGetToken import GHGetToken
from github import Github, Repository, Issue, Label


class GHRepository:
    def __init__(self, gh_token: GHGetToken, gh_repo: str) -> None:
        self.connector = gh_token.connector
        self.repo: Repository.Repository = self.connector.get_repo(gh_repo)

    def get_project_data(self, label: Label.Label):
        data = {
            "repo_id": self.repo.id,
            "name": label.name,
        }
        print(f"label data {data}")
        return data
