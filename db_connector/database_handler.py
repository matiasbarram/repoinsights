from .connector import DBConnector
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
)
from github_service.github_api.commit import GHCommit
from github_service.github_api.user import GHUser
from github_service.github_api.repository import GHRepository
from github_service.github_api.pull_request import GHPullRequest
from pprint import pprint
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from typing import Union, List


class DatabaseHandler:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.Session_consolidada = sessionmaker(bind=connector.consolidada_engine)
        self.session_consolidada = self.Session_consolidada()

        self.Session_temp = sessionmaker(bind=connector.temp_engine)
        self.session_temp = self.Session_temp()

    def create_watchers(self, watchers: List[GHUser], project_id: int):
        watchers_db = []
        for watcher in watchers:
            exist_user = (
                self.session_temp.query(User).filter_by(login=watcher.login).first()
            )
            if not exist_user:
                user_id = self.create_user(watcher)
                watchers_db.append(
                    {
                        "repo_id": project_id,
                        "user_id": user_id,
                        "created_at": watcher.created_at,
                    }
                )
        self.session_temp.add_all(watchers_db)

    def create_project(self, repository: GHRepository):
        existing_project = (
            self.session_temp.query(Project).filter_by(name=repository.name).first()
        )
        if existing_project:
            return int(existing_project.id)  # type: ignore
        else:
            new_project = Project(**repository.to_dict())
            self.session_temp.add(new_project)
            self.session_temp.commit()
            return int(new_project.id)  # type: ignore

    def create_user(self, user: GHUser) -> int:
        existing_user = (
            self.session_temp.query(User).filter_by(login=user.login).first()
        )
        if existing_user:
            return int(existing_user.id)  # type: ignore
        else:
            new_user = User(**user.to_dict())
            self.session_temp.add(new_user)
            self.session_temp.commit()
            return int(new_user.id)  # type: ignore

    def create_commit(self, commit: GHCommit):
        commit_id = None
        existing_commit = (
            self.session_temp.query(Commit).filter_by(sha=commit.sha).first()
        )
        if existing_commit:
            commit_id = int(existing_commit.id)  # type: ignore
        else:
            new_commit = Commit(**commit.db_commit())
            self.session_temp.add(new_commit)
            self.session_temp.commit()
            commit_id = int(new_commit.id)  # type: ignore

        return commit_id

    def create_commit_parents(self, commit_id: int, parents: list):
        parent_sha: str
        commits_parents = []
        for parent_sha in parents:
            exist_parent_commit = (
                self.session_temp.query(Commit).filter_by(sha=parent_sha).first()
            )
            if exist_parent_commit:
                exist_relation = (
                    self.session_temp.query(CommitParent)
                    .filter_by(
                        commit_id=commit_id, parent_id=int(exist_parent_commit.id)  # type: ignore
                    )
                    .first()
                )
                if not exist_relation:
                    parent_id = int(exist_parent_commit.id)  # type: ignore
                    commits_parents.append(
                        CommitParent(commit_id=commit_id, parent_id=parent_id)
                    )
                else:
                    print(f"Relation commit-parent already exist")
            else:
                print(f"Commit with sha {parent_sha} not found")

        self.session_temp.add_all(commits_parents)

    def create_pull_request(self, pr: GHPullRequest):
        exist_pr = (
            self.session_temp.query(PullRequest).filter_by(pullreq_id=pr.number).first()
        )
        if exist_pr:
            print(f"Pull request {pr.number} already exist")
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
