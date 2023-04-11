from typing import List
from github.PullRequest import PullRequest
from github.Repository import Repository
from ..pull_request import GHPullRequest
from ..comment import GHPullRequestComment
from datetime import datetime


class PullRequestHandler:
    def __init__(self, repo: Repository):
        self.repo = repo

    def get_all_pull_requests(self) -> List[GHPullRequest]:
        pull_requests = self.repo.get_pulls(state="all")
        pull_request_objects = [GHPullRequest(pr) for pr in pull_requests]
        return pull_request_objects

    def get_pull_requests_between_dates(
        self, start_date: datetime, end_date: datetime
    ) -> List[GHPullRequest]:
        pull_requests = self.repo.get_pulls(state="all")
        pull_requests_between_dates = []
        for pr in pull_requests:
            created_at = pr.created_at
            if start_date <= created_at <= end_date:
                pull_requests_between_dates.append(GHPullRequest(pr))
        return pull_requests_between_dates

    def get_pull_request_comments(
        self, pull_request: GHPullRequest
    ) -> List[GHPullRequestComment]:
        comments = pull_request.get_comments()
        return comments
