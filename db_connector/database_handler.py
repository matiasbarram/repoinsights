from .connector import DBConnector
from .models import (
    User,
    Project,
    Commit,
    CommitParent,
    Issue,
    IssueComment,
    PullRequest,
    PullRequestComment,
    Watcher,
)
from github_service.repoinsights.commit import InsightsCommit
from github_service.repoinsights.user import InsightsUser
from github_service.repoinsights.repository import InsightsRepository
from github_service.repoinsights.pull_request import GHPullRequest
from github_service.repoinsights.isssue import InsightsIssue
from pprint import pprint
from sqlalchemy.orm import sessionmaker
from typing import Union, List, Optional
from loguru import logger


class DatabaseHandler:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.Session_consolidada = sessionmaker(bind=connector.consolidada_engine)
        self.session_consolidada = self.Session_consolidada()

        self.Session_temp = sessionmaker(bind=connector.temp_engine)
        self.session_temp = self.Session_temp()

    def get_or_create(
        self,
        model: Union[
            User,
            Project,
            Commit,
            CommitParent,
            Issue,
            IssueComment,
            PullRequest,
            PullRequestComment,
            Watcher,
        ],
        create: Optional[bool] = True,
        **kwargs,
    ):
        instance = self.session_temp.query(model).filter_by(**kwargs).first()
        if instance:
            logger.debug("Instance already exists")
            return instance
        elif create:
            try:
                logger.debug("Creating new instance")
                instance = model(**kwargs)
                self.session_temp.add(instance)
                self.session_temp.commit()
                return instance
            except Exception as e:
                logger.error(f"Error creating")
                raise BaseException(e)
        else:
            logger.debug("Instance does not exist and not creating")
            return None

    def create_watchers(self, watchers: List[InsightsUser], project_id: int):
        watchers_db = []
        watcher: InsightsUser
        for watcher in watchers:
            user = self.get_or_create(User, **watcher.to_dict())
            user_id = int(user.id)  # type: ignore

            existing_watcher = (
                self.session_temp.query(Watcher)
                .filter_by(repo_id=project_id, user_id=user_id)
                .first()
            )
            if not existing_watcher:
                new_watcher = Watcher(
                    repo_id=project_id, user_id=user_id, created_at=watcher.created_at
                )
                watchers_db.append(new_watcher)

        self.session_temp.add_all(watchers_db)
        self.session_temp.commit()

    def create_project(self, repository: InsightsRepository):
        existing_project = self.get_or_create(Project, **repository.to_dict())
        return int(existing_project.id)  # type: ignore

    def create_user(self, user: InsightsUser) -> int:
        existing_user = self.get_or_create(User, **user.to_dict())
        return int(existing_user.id)  # type: ignore

    def create_commit(self, commit: InsightsCommit):
        existing_commit = self.get_or_create(Commit, **commit.to_dict())
        return int(existing_commit.id)  # type: ignore

    def create_commit_parent_relation(self, commit_id: int, parent_id: int):
        existing_relation = (
            self.session_temp.query(CommitParent)
            .filter_by(commit_id=commit_id, parent_id=parent_id)
            .first()
        )
        if not existing_relation:
            new_relation = CommitParent(commit_id=commit_id, parent_id=parent_id)
            self.session_temp.add(new_relation)
            return new_relation
        else:
            logger.warning(
                f"Relation commit-parent already exists: {commit_id} - {parent_id}"
            )
            return None

    def create_commit_parents(self, commit_id: int, parents: list):
        parent_sha: str
        commits_parents = []
        for parent_sha in parents:
            parent_commit = self.get_or_create(Commit, sha=parent_sha)
            parent_id = int(parent_commit.id)  # type: ignore

            commit_parent_relation = self.create_commit_parent_relation(
                commit_id, parent_id
            )
            if commit_parent_relation:
                commits_parents.append(commit_parent_relation)
            else:
                logger.info(f"Parent commit not found: {parent_sha}")

        self.session_temp.add_all(commits_parents)
        self.session_temp.commit()

    def create_pull_request(self, pr: GHPullRequest):
        existing_pr = self.get_or_create(PullRequest, **pr.to_dict())
        return int(existing_pr.id)  # type: ignore

    def create_issue(self, issue: InsightsIssue):
        existing_issue = self.get_or_create(Issue, **issue.to_dict())
        return int(existing_issue.id)  # type: ignore

    def find_pr_id(self, **kwargs) -> int:
        pr = self.get_or_create(PullRequest, create=False, **kwargs)
        return int(pr.id)  # type: ignore

    def close(self):
        self.session_temp.close()
