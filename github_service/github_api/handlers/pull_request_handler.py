from typing import List, Union, Optional
from github.PullRequest import PullRequest
from github.Repository import Repository
from ..pull_request import GHPullRequest
from ..comment import GHPullRequestComment
from ..commit import GHCommit
from datetime import datetime


class PullRequestHandler:
    def __init__(self, repo: Repository):
        self.repo = repo

    def get_all_pull_requests(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> List[GHPullRequest]:
        pull_requests = self.repo.get_pulls(state="all")

        if start_date is None or end_date is None:
            return [self._process_pull_request(pr) for pr in pull_requests]

        pull_requests_between_dates = [
            self._process_pull_request(pr)
            for pr in pull_requests
            if start_date <= pr.created_at <= end_date
        ]
        return pull_requests_between_dates

    def get_pull_request_comments(
        self, pull_request: GHPullRequest
    ) -> List[GHPullRequestComment]:
        return pull_request.get_comments()

    def _process_pull_request(self, pr: PullRequest) -> GHPullRequest:
        gh_pr = GHPullRequest(pr)
        self.set_pull_request_commits(gh_pr)
        return gh_pr

    def set_pull_request_commits(self, pull_request: GHPullRequest) -> None:
        base_commit = GHCommit(self.repo.get_commit(pull_request.base_commit_sha))
        head_commit = GHCommit(self.repo.get_commit(pull_request.head_commit_sha))
        pull_request.set_base_commit(base_commit)
        pull_request.set_head_commit(head_commit)
