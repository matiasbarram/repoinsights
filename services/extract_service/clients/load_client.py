from services.extract_service.repoinsights.commit import InsightsCommit
from services.extract_service.repoinsights.repository import InsightsRepository
from services.extract_service.repoinsights.pull_request import InsightsPullRequest
from services.extract_service.repoinsights.milestone import InsightsMilestone
from services.extract_service.repoinsights.comment import (
    InsightsCommitComment,
    InsightsPullRequestComment,
    InsightsIssueComment,
)
from services.extract_service.repoinsights.label import InsightsLabel
from services.extract_service.repoinsights.user import InsightsUser
from services.extract_service.repoinsights.isssue import InsightsIssue
from services.extract_service.repoinsights.issue_event import InsightsIssueEvent
from services.extract_service.db_connector.connector import DBConnector
from services.extract_service.db_connector.database_handler import DatabaseHandler

from typing import List, Union, Dict, Any
from loguru import logger


class MainProjectError(Exception):
    pass


class ExtractDataResulstsError(Exception):
    pass


class LoadDataClient:
    def __init__(self, results: List[Dict[str, Any]], uuid: str) -> None:
        self.temp_db = DatabaseHandler(DBConnector("temp"), uuid)
        self.sorted_results = self.sort_results(results)

    def sort_results(self, results: List[Dict[str, Any]]):
        order = {
            "project": 0,
            "labels": 1,
            "owner": 2,
            "commit": 3,
            "pull_request": 4,
            "issue": 5,
            "watchers": 6,
            "members": 7,
            "milestones": 8,
        }
        try:
            self.sorted_results = sorted(results, key=lambda x: order[x["name"]])
            return self.sorted_results
        except KeyError as e:
            raise ExtractDataResulstsError(
                f"Results must contain a 'name' key. Error: {e}"
            )

    def load_to_temp_db(self):
        for result in self.sorted_results:
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
            elif name == "milestones":
                self.load_milestones_data(data)

    def load_main_project(self, repo_data: Dict[str, Any]):
        self.repository = InsightsRepository(repo_data)
        self.repository.set_owner_id(self.load_user(self.repository.owner))
        self.repo_id = self.repository.set_repo_id(
            self.load_repository(self.repository)
        )
        self.project_id = self.load_extraction_project(self.repository.id)

    def load_extraction_project(self, repo_id: int):
        logger.debug(
            "Loading extraction project for repository {name}",
            name=self.repository.name,
        )
        return self.temp_db.create_extraction_project(repo_id)

    def load_milestones_data(self, milestones: List[InsightsMilestone]):
        logger.debug(
            "Loading milestones for repository {name}", name=self.repository.name
        )
        milestone: InsightsMilestone
        for milestone in milestones:
            milestone.set_repo_id(self.repo_id)  # type: ignore
            self.temp_db.create_milestone(milestone)

    def load_labels_data(self, labels: List[InsightsLabel]):
        logger.debug("Loading labels for repository {name}", name=self.repository.name)
        label: InsightsLabel
        for label in labels:
            label.set_project_id(self.repo_id)
            self.temp_db.create_label(label)

    def load_issue_labels(self, project_id, issue_id, labels: List[InsightsLabel]):
        logger.debug("Loading issue labels")
        label: InsightsLabel
        for label in labels:
            label.set_project_id(project_id)
            label_id = self.temp_db.create_label(label)
            self.temp_db.create_issue_label_relation(issue_id, label_id)

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
        commit_id = self.temp_db.create_commit(commit)
        self.temp_db.create_project_commit(commit.project_id, commit_id)
        return commit_id

    def load_pull_request(self, pr: InsightsPullRequest):
        logger.debug("Loading pull request {number}", number=pr.number)
        return self.temp_db.create_pull_request(pr)

    def load_watchers(self, watchers: List[InsightsUser]):
        logger.debug(
            "Loading watchers for repository {name}", name=self.repository.name
        )
        self.temp_db.create_watchers(watchers, self.repository.id)

    def load_pull_request_comments(
        self, pr, pr_id, comments: List[InsightsPullRequestComment]
    ):
        for comment in comments:
            comment.set_pull_request_id(pr_id)
            # TODO - this is a hack, we need to fix this in the future
            # se debe cambiar en el schema.sql que el user_id sea nullable
            if comment.author is not None:
                comment.set_user_id(self.load_user(comment.author))
                commit_id = self.find_commit_sha(comment.commit_sha)
                comment.set_commit_id(commit_id)
                self.temp_db.create_pull_request_comment(comment)
            else:
                logger.error("Comment {id} has no author, skipping", id=comment)

    def load_pull_request_history(self, pr: InsightsPullRequest, pr_id):
        if pr.created_at is not None:
            data = {
                "pull_request_id": pr_id,
                "created_at": pr.created_at,
                "action": "opened",
                "actor_id": self.load_user(pr.author),
            }
            self.temp_db.create_pull_request_history(data)
        if pr.closed_at is not None:
            data = {
                "pull_request_id": pr_id,
                "created_at": pr.closed_at,
                "action": "closed",
                "actor_id": self.load_user(pr.author),
            }
            self.temp_db.create_pull_request_history(data)
        if pr.merged_at is not None:
            data = {
                "pull_request_id": pr_id,
                "created_at": pr.merged_at,
                "action": "merged",
                "actor_id": self.load_user(pr.author),
            }
            self.temp_db.create_pull_request_history(data)

    def load_issues_data(self, issues: List[InsightsIssue]):
        for issue in issues:
            project_id = issue.set_project_id(self.repository.id)
            issue.set_reporter_id(self.load_user(issue.reporter))
            if issue.assignee:
                issue.set_assignee_id(self.load_user(issue.assignee))
            self.set_pr_id(issue)
            issue_id = self.temp_db.create_issue(issue)
            self.load_issue_labels(project_id, issue_id, issue.labels)
            comment: InsightsIssueComment
            for comment in issue.comments:
                comment.set_issue_id(issue_id)
                if comment.author:
                    comment.set_user_id(self.load_user(comment.author))
                self.temp_db.create_issue_comment(comment)
            event: InsightsIssueEvent
            for event in issue.events:
                event.set_issue_id(issue_id)
                if event.actor:
                    event.set_actor_id(self.load_user(event.actor))
                    self.temp_db.create_issue_event(event)
                else:
                    logger.error("Event without actor")

    def load_commits_data(self, commits: List[InsightsCommit]):
        commit: InsightsCommit
        for commit in commits:
            commit.set_project_id(self.repository.id)
            commit.set_author_id(
                self.load_user(commit.author) if commit.author else None
            )
            commit.set_committer_id(
                self.load_user(commit.committer) if commit.committer else None
            )
            commit_id = self.load_commit(commit)
            self.temp_db.create_commit_comments(commit_id, commit.comments)
            # self.temp_db.create_commit_parents(commit_id, commit.parents)

    def load_watchers_data(self, watchers: List[InsightsUser]):
        self.load_watchers(watchers)

    def load_pull_requests_data(self, pull_requests: List[InsightsPullRequest]):
        for pr in pull_requests:
            pr.set_user_id(self.load_user(pr.author))
            self.update_repo_data(pr.head_repo)
            self.update_repo_data(pr.base_repo)
            self.update_commit_data(pr.head_commit)
            self.update_commit_data(pr.base_commit)
            head_commit_id = self.load_commit(pr.head_commit)
            base_commit_id = self.load_commit(pr.base_commit)
            pr.set_head_commit_id(head_commit_id)
            pr.set_base_commit_id(base_commit_id)
            if pr.head_repo is not None:
                pr.set_head_repo_id(self.load_repository(pr.head_repo))
            if pr.base_repo is not None:
                pr.set_base_repo_id(self.load_repository(pr.base_repo))
            pr_id = self.load_pull_request(pr)
            self.load_pull_request_comments(pr, pr_id, pr.comments)
            self.load_pull_request_history(pr, pr_id)

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

    def find_commit_sha(self, sha: str) -> Union[int, None]:
        return self.temp_db.find_commit_id(
            sha=sha,
        )

    def get_project_id(self) -> int:
        return self.repository.id
