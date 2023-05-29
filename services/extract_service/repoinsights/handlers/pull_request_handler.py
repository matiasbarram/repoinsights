from typing import List, Union, Optional, Dict, Any
from ..pull_request import InsightsPullRequest
from ..comment import InsightsPullRequestComment
from ..commit import InsightsCommit
from datetime import datetime
from services.extract_service.extract_module.extract_client import GitHubExtractor
from ...utils.utils import api_date, get_int_from_dict
from pprint import pprint


class InsightsPullRequestHandler:
    def __init__(self, repo: GitHubExtractor):
        self.repo = repo

    def get_all_pull_requests(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> List[InsightsPullRequest]:
        pull_requests = self.repo.obtener_pull_requests(
            state="all", since=start_date, until=end_date
        )

        return [self._process_pull_request(pr) for pr in pull_requests]

    def _process_pull_request(self, pr: Dict[str, Any]):
        gh_pr = InsightsPullRequest(pr)
        self.set_pull_request_commits(gh_pr)
        return gh_pr

    def set_pull_request_commits(self, pull_request: InsightsPullRequest) -> None:
        base_commit = InsightsCommit(
            self.repo.obtener_commit(pull_request.base_commit_sha)
        )
        head_commit = InsightsCommit(
            self.repo.obtener_commit(pull_request.head_commit_sha)
        )
        pull_request.set_base_commit(base_commit)
        pull_request.set_head_commit(head_commit)

    def get_pull_request_comments(self, pull_requests: List[InsightsPullRequest]):
        comments = self.repo.obtener_pull_requests_comments()
        for pull_request in pull_requests:
            pull_request_comments = [
                InsightsPullRequestComment(comment)
                for comment in comments
                if get_int_from_dict(comment, "pull_request_url") == pull_request.number
            ]
            pull_request.set_comments(pull_request_comments)
