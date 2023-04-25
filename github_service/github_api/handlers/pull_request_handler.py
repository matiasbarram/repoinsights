from typing import List, Union, Optional, Dict, Any
from ..pull_request import GHPullRequest
from ..comment import GHPullRequestComment
from ..commit import GHCommit
from datetime import datetime
from ...github import GitHubExtractor
from ...utils.utils import gh_api_to_datetime


class PullRequestHandler:
    def __init__(self, repo: GitHubExtractor):
        self.repo = repo

    def get_all_pull_requests(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> List[GHPullRequest]:
        pull_requests = self.repo.obtener_pull_requests(
            state="all", since=start_date, until=end_date
        )

        return [self._process_pull_request(pr) for pr in pull_requests]

    # def get_pull_request_comments(
    #     self, pull_request: GHPullRequest
    # ) -> List[GHPullRequestComment]:
    #     return pull_request.get_comments()

    def _process_pull_request(self, pr: Dict[str, Any]):
        gh_pr = GHPullRequest(pr)
        self.set_pull_request_commits(gh_pr)
        return gh_pr

    def set_pull_request_commits(self, pull_request: GHPullRequest) -> None:
        base_commit = GHCommit(self.repo.obtener_commit(pull_request.base_commit_sha))
        head_commit = GHCommit(self.repo.obtener_commit(pull_request.head_commit_sha))
        pull_request.set_base_commit(base_commit)
        pull_request.set_head_commit(head_commit)
