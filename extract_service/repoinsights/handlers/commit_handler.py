from datetime import datetime
from typing import Union
from ..comment import InsightsCommitComment
from ..commit import InsightsCommit
from loguru import logger
from typing import Any, Dict
from ...github_api.extractor import GitHubExtractor


class InsightsCommitHandler:
    def __init__(self, repo: GitHubExtractor):
        self.repo = repo

    def get_commits(self, since: Union[None, datetime], until: Union[None, datetime]):
        kwargs = {}
        if since:
            kwargs["since"] = since
        if until:
            kwargs["until"] = until

        commits = self.repo.obtener_commits(**kwargs)
        return [InsightsCommit(commit) for commit in commits]

    def get_commit(self, commit_sha: str):
        commit = self.repo.obtener_commit(commit_sha)
        return InsightsCommit(commit)

    # def get_commit_comments(self, commit_sha: str):
    #     comments = self.repo.get_commit(commit_sha).get_comments()
    #     return [GHCommitComment(comment) for comment in comments]

    # def get_commit_parents(self, commit_sha: str):
    #     parents = self.repo.get_commit(commit_sha).parents
    #     return [GHCommit(parent) for parent in parents]
