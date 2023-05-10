import datetime
from services.traspaso_service.db_connector.models import (
    User,
    Project,
    Commit,
    CommitComment,
    CommitParent,
    Follower,
    Fork,
    Issue,
    IssueComment,
    IssueEvent,
    IssueLabel,
    OrganizationMember,
    ProjectCommit,
    ProjectMember,
    PullRequest,
    PullRequestComment,
    PullRequestCommit,
    PullRequestHistory,
    RepoLabel,
    RepoMilestone,
    Watcher,
    Extraction,
)
from services.traspaso_service.db_connector.database_handler import DatabaseHandler
import pandas as pd
from sqlalchemy.orm import Session
from pandas import Series, DataFrame
from pprint import pprint
from loguru import logger
import csv
from typing import List
import copy


class TempClient:
    def __init__(self, db: DatabaseHandler, uuid) -> None:
        self.db = db
        self.uuid = uuid

    def get_users(self) -> List[User]:
        users = self.db.session_temp.query(User).filter_by(ext_ref_id=self.uuid).all()
        return users

    def get_projects(self) -> List[Project]:
        projects = (
            self.db.session_temp.query(Project).filter_by(ext_ref_id=self.uuid).all()
        )
        return projects

    def get_extractions(self) -> List[Extraction]:
        extractions = (
            self.db.session_temp.query(Extraction).filter_by(ext_ref_id=self.uuid).all()
        )
        return extractions

    def get_project_members(self) -> List[ProjectMember]:
        project_members = (
            self.db.session_temp.query(ProjectMember)
            .filter_by(ext_ref_id=self.uuid)
            .all()
        )
        return project_members

    def get_commits(self) -> List[Commit]:
        commits = (
            self.db.session_temp.query(Commit).filter_by(ext_ref_id=self.uuid).all()
        )
        return commits

    def get_issues(self) -> List[Issue]:
        issues = self.db.session_temp.query(Issue).filter_by(ext_ref_id=self.uuid).all()
        return issues

    def get_prs(self) -> List[PullRequest]:
        prs = (
            self.db.session_temp.query(PullRequest)
            .filter_by(ext_ref_id=self.uuid)
            .all()
        )
        return prs

    def get_commit_comments(self) -> List[CommitComment]:
        commit_comments = (
            self.db.session_temp.query(CommitComment)
            .filter_by(ext_ref_id=self.uuid)
            .all()
        )
        return commit_comments

    def get_commit_parents(self) -> List[CommitParent]:
        commit_parents = (
            self.db.session_temp.query(CommitParent)
            .filter_by(ext_ref_id=self.uuid)
            .all()
        )
        return commit_parents

    def get_issue_comments(self) -> List[IssueComment]:
        issue_comments = (
            self.db.session_temp.query(IssueComment)
            .filter_by(ext_ref_id=self.uuid)
            .all()
        )
        return issue_comments

    def get_issue_events(self) -> List[IssueEvent]:
        issue_events = (
            self.db.session_temp.query(IssueEvent).filter_by(ext_ref_id=self.uuid).all()
        )
        return issue_events

    def get_issue_labels(self) -> List[IssueLabel]:
        issue_labels = (
            self.db.session_temp.query(IssueLabel).filter_by(ext_ref_id=self.uuid).all()
        )
        return issue_labels

    def get_pr_comments(self) -> List[PullRequestComment]:
        pr_comments = (
            self.db.session_temp.query(PullRequestComment)
            .filter_by(ext_ref_id=self.uuid)
            .all()
        )
        return pr_comments

    def get_pr_history(self) -> List[PullRequestHistory]:
        pr_history = (
            self.db.session_temp.query(PullRequestHistory)
            .filter_by(ext_ref_id=self.uuid)
            .all()
        )
        return pr_history

    def get_labels(self) -> List[RepoLabel]:
        labels = (
            self.db.session_temp.query(RepoLabel).filter_by(ext_ref_id=self.uuid).all()
        )
        return labels

    def get_milestones(self) -> List[RepoMilestone]:
        milestones = (
            self.db.session_temp.query(RepoMilestone)
            .filter_by(ext_ref_id=self.uuid)
            .all()
        )
        return milestones

    def get_watchers(self) -> List[Watcher]:
        watchers = (
            self.db.session_temp.query(Watcher).filter_by(ext_ref_id=self.uuid).all()
        )
        return watchers

    def get_followers(self) -> List[Follower]:
        followers = (
            self.db.session_temp.query(Follower).filter_by(ext_ref_id=self.uuid).all()
        )
        return followers
