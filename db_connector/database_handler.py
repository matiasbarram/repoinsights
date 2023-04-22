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
from github_service.github_api.commit import GHCommit
from github_service.github_api.user import GHUser
from github_service.github_api.repository import GHRepository
from github_service.github_api.pull_request import GHPullRequest
from pprint import pprint
from sqlalchemy.orm import sessionmaker
from typing import Union, List
from loguru import logger


class DatabaseHandler:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.Session_consolidada = sessionmaker(bind=connector.consolidada_engine)
        self.session_consolidada = self.Session_consolidada()

        self.Session_temp = sessionmaker(bind=connector.temp_engine)
        self.session_temp = self.Session_temp()

    def get_or_create(self, model, **kwargs):
        instance = self.session_temp.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            self.session_temp.add(instance)
            self.session_temp.commit()
            return instance

    def create_watchers(self, watchers: List[GHUser], project_id: int):
        watchers_db = []
        watcher: GHUser
        for watcher in watchers:
            user = self.get_or_create(User, login=watcher.login)
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

    def create_project(self, repository: GHRepository):
        existing_project = self.get_or_create(
            Project, name=repository.name, owner_id=repository.owner_id
        )
        return int(existing_project.id)  # type: ignore

    def create_user(self, user: GHUser) -> int:
        existing_user = self.get_or_create(User, login=user.login)
        return int(existing_user.id)  # type: ignore

    def create_commit(self, commit: GHCommit):
        existing_commit = self.get_or_create(Commit, sha=commit.sha)
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
            logger.info(
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
        exist_pr = (
            self.session_temp.query(PullRequest).filter_by(pullreq_id=pr.number).first()
        )
        if exist_pr:
            logger.info(
                f"Pull request already exist: {pr.number} - {pr.head_repo_id} - {pr.base_repo_id}"
            )
        else:
            self.session_temp.add(
                PullRequest(
                    head_repo_id=pr.head_repo_id,
                    base_repo_id=pr.base_repo_id,
                    head_commit_id=pr.head_commit_id,
                    base_commit_id=pr.base_commit_id,
                    pullreq_id=pr.number,
                    user_id=pr.user_id,
                    intra_branch=pr.intra_branch,
                    merged=pr.merged,
                )
            )
            self.session_temp.commit()

    def close(self):
        self.session_temp.close()
