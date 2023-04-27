from extract_service.repoinsights.commit import InsightsCommit
from extract_service.repoinsights.repository import InsightsRepository
from extract_service.repoinsights.pull_request import GHPullRequest
from extract_service.repoinsights.label import InsightsLabel
from extract_service.repoinsights.user import InsightsUser
from extract_service.repoinsights.isssue import InsightsIssue
from extract_service.db_connector.connector import DBConnector
from extract_service.db_connector.database_handler import DatabaseHandler

from typing import List, Union, Dict, Any
from loguru import logger


class MainProjectError(Exception):
    pass


class LoadDataClient:
    def __init__(self, results: List[Dict[str, Any]]) -> None:
        self.temp_db = DatabaseHandler(DBConnector())
        self.results = results

    def load_data(self):
        order = {
            "project": 0,
            "owner": 1,
            "commit": 2,
            "pull_request": 3,
            "issue": 4,
            "watchers": 5,
            "members": 6,
            # "labels": 6,
        }
        sorted_results = sorted(self.results, key=lambda x: order[x["name"]])
        for result in sorted_results:
            name, data = result["name"], result["data"]
            logger.critical(f"Loading {name}")
            if name == "project":
                self.load_main_project(data)
            if name == "commit":
                self.load_commits_data(data)
            elif name == "watchers":
                self.load_watchers_data(data)
            elif name == "pull_request":
                self.load_pull_requests_data(data)
            elif name == "issue":
                self.load_issues_data(data)
            elif name == "labels":
                self.load_labels_data(data)
            elif name == "members":
                self.load_members_data(data)

    def load_main_project(self, repo_data: Dict[str, Any]):
        self.repository = InsightsRepository(repo_data)
        self.repository.set_owner_id(self.load_user(self.repository.owner))
        self.repo_id = self.repository.set_repo_id(
            self.load_repository(self.repository)
        )

    def load_labels_data(self, labels: List[InsightsLabel]):
        logger.debug("Loading labels for repository {name}", name=self.repository.name)

    def load_members_data(self, members: List[InsightsUser]):
        logger.debug("Loading members for repository {name}", name=self.repository.name)
        for member in members:
            user_id = self.load_user(member)
            member_data = {
                "user_id": user_id,
                "project_id": self.repository.id,
            }
            return self.temp_db.create_members(member_data)

    def load_repository(self, repository: InsightsRepository):
        logger.debug(
            "Loading repository {owner} {name}",
            owner=repository.owner.login,
            name=repository.name,
        )
        return self.temp_db.create_project(repository)

    def load_user(self, user: InsightsUser) -> int:
        logger.debug("Loading user {login}", login=user.login)
        return self.temp_db.create_user(user)

    def load_commit(self, commit: InsightsCommit) -> int:
        logger.debug("Loading commit {sha}", sha=commit.sha)
        return self.temp_db.create_commit(commit)

    def load_pull_request(self, pr: GHPullRequest):
        logger.debug("Loading pull request {number}", number=pr.number)
        self.temp_db.create_pull_request(pr)

    def load_watchers(self, watchers: List[InsightsUser]):
        logger.debug(
            "Loading watchers for repository {name}", name=self.repository.name
        )
        self.temp_db.create_watchers(watchers, self.repository.id)

    def load_issues_data(self, issues: List[InsightsIssue]):
        for issue in issues:
            issue.set_project_id(self.repository.id)
            issue.set_reporter_id(self.load_user(issue.reporter))
            if issue.assignee:
                issue.set_assignee_id(self.load_user(issue.assignee))
            self.set_pr_id(issue)
            self.temp_db.create_issue(issue)

    def load_commits_data(self, commits: List[InsightsCommit]):
        for commit in commits:
            commit.set_project_id(self.repository.id)
            commit.set_author_id(
                self.load_user(commit.author) if commit.author else None
            )
            commit.set_committer_id(
                self.load_user(commit.committer) if commit.committer else None
            )
            commit_id = self.load_commit(commit)
            # self.temp_db.create_commit_parents(commit_id, commit.parents)

    def load_watchers_data(self, watchers: List[InsightsUser]):
        self.load_watchers(watchers)

    def load_pull_requests_data(self, pull_requests: List[GHPullRequest]):
        for pr in pull_requests:
            pr.set_user_id(self.load_user(pr.author))
            self.update_repo_data(pr.head_repo)
            self.update_repo_data(pr.base_repo)
            self.update_commit_data(pr.head_commit)
            self.update_commit_data(pr.base_commit)
            pr.set_head_commit_id(self.load_commit(pr.head_commit))
            pr.set_base_commit_id(self.load_commit(pr.base_commit))
            if pr.head_repo is not None:
                pr.set_head_repo_id(self.load_repository(pr.head_repo))
            if pr.base_repo is not None:
                pr.set_base_repo_id(self.load_repository(pr.base_repo))
            self.load_pull_request(pr)

    def update_repo_data(self, pr_repo: Union[InsightsRepository, None]):
        if pr_repo is None:
            return

        if pr_repo.forked_from is True:
            pr_repo.set_forked_from_id(self.repository.id)
        if pr_repo.raw_repo["owner"] is not None:
            pr_repo.set_owner_id(self.load_user(pr_repo.owner))

    def update_commit_data(self, pr_commit: InsightsCommit):
        pr_commit.set_project_id(self.repository.id)
        if pr_commit.author is None:
            pr_commit.set_author_id(None)
        else:
            pr_commit.set_author_id(self.load_user(pr_commit.author))

        if pr_commit.committer is None:
            pr_commit.set_committer_id(None)
        else:
            pr_commit.set_committer_id(self.load_user(pr_commit.committer))

    def set_pr_id(self, issue: InsightsIssue) -> None:
        if issue.pull_request is None or issue.pull_request == False:
            return
        else:
            pr_id = self.temp_db.find_pr_id(
                pullreq_id=issue.issue_id, base_repo_id=self.repo_id
            )
            if pr_id:
                issue.set_pull_requests_id(pr_id)
