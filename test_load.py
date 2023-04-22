from db_connector.connector import DBConnector
from db_connector.database_handler import DatabaseHandler
from github_service.github_api.client import GitHubClient
from github_service.github_api.commit import GHCommit
from github_service.github_api.repository import GHRepository
from github_service.github_api.pull_request import GHPullRequest
from github_service.github_api.user import GHUser
from pprint import pprint
import json


class LoadData:
    def __init__(self, client: GitHubClient):
        self.temp_db = DatabaseHandler(DBConnector())
        self.repository = client.repository

    def load_repository(self, repository: GHRepository):
        return self.temp_db.create_project(repository)

    def load_commit_comments(self, commit_id: int, commit: GHCommit):
        if commit.comments:
            print(commit.comments)
            print("TODO - Load commit comments")

    def load_commit_parents(self, commit_id: int, commit: GHCommit):
        if commit.parents:
            self.temp_db.create_commit_parents(commit_id, commit.parents)

    def load_temp_db(self, results):
        for result in results:
            if result["name"] == "owner":
                gh_user: GHUser = result["data"]
                owner_id = self.temp_db.create_user(gh_user)
                self.repository.set_owner_id(owner_id)
                project_id = self.load_repository(self.repository)
                self.repository.set_repo_id(project_id)

            if result["name"] == "commit":
                commit: GHCommit
                for commit in result["data"]:
                    commit.set_project_id(self.repository.id)
                    author_id = (
                        self.temp_db.create_user(commit.author)
                        if commit.author
                        else None
                    )
                    committer_id = (
                        self.temp_db.create_user(commit.committer)
                        if commit.committer
                        else None
                    )
                    commit.set_committer_id(committer_id)
                    commit.set_author_id(author_id)
                    commit_id = self.temp_db.create_commit(commit)
                    self.load_commit_comments(commit_id, commit)
                    self.load_commit_parents(commit_id, commit)  # type: ignore

            if result["name"] == "watchers":
                self.temp_db.create_watchers(result["data"], self.repository.id)

            if result["name"] == "pull_request":
                pull_request: GHPullRequest
                for pull_request in result["data"]:
                    author_id = self.temp_db.create_user(pull_request.author)
                    pull_request.set_user_id(author_id)

                    self.set_repo_data(pull_request.head_repo)
                    head_repo_id = self.temp_db.create_project(pull_request.head_repo)

                    self.set_repo_data(pull_request.base_repo)
                    base_repo_id = self.temp_db.create_project(pull_request.base_repo)

                    pull_request.set_head_repo_id(head_repo_id)
                    pull_request.set_base_repo_id(base_repo_id)

                    self.set_commit_data(pull_request.head_commit)
                    self.set_commit_data(pull_request.base_commit)

                    head_commit_id = self.temp_db.create_commit(
                        pull_request.head_commit
                    )
                    base_commit_id = self.temp_db.create_commit(
                        pull_request.base_commit
                    )

                    pull_request.set_head_commit_id(head_commit_id)
                    pull_request.set_base_commit_id(base_commit_id)
                    self.temp_db.create_pull_request(pull_request)

    def set_repo_data(self, pr_repo: GHRepository):
        if pr_repo.forked_from is not None:
            pr_repo.set_forked_from_id(self.repository.id)
        if pr_repo.raw_repo["owner"] is not None:
            user_id = self.temp_db.create_user(pr_repo.owner)
            pr_repo.set_owner_id(user_id)

    def set_commit_data(self, pr_commit: GHCommit):
        pr_commit.set_project_id(self.repository.id)
        if pr_commit.author is None:
            pr_commit.set_author_id(None)
        else:
            author_id = self.temp_db.create_user(pr_commit.author)
            pr_commit.set_author_id(author_id)

        if pr_commit.committer is None:
            pr_commit.set_committer_id(None)
        else:
            committer_id = self.temp_db.create_user(pr_commit.committer)
            pr_commit.set_committer_id(committer_id)
