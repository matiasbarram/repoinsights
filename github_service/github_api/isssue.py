from datetime import datetime
from github.Repository import Repository
from github.Issue import Issue
from .comment import GHIssueComment
from .label import GHLabel


class GHIssue:
    def __init__(self, issue: Issue) -> None:
        self.id = issue.id
        self.reporter_id = issue.assignee
        self.pull_request = issue.pull_request
        self.pull_request_id = issue.id
        self.created_at = issue.closed_by
        self.updated_at = issue.updated_at
        self.closed_at = issue.closed_at
        self.title = issue.title
        self.state = issue.state
        self.number = issue.number
        self.labels = []

    def set_labels(self, labels):
        self.labels = [GHLabel(label) for label in labels]

    def get_labels(self):
        print("Getting labels")
        return self.labels

    def set_comments(self, comments: list[GHIssueComment]):
        self.comments = comments

    def get_comments(self) -> list[GHIssueComment]:
        return self.comments
