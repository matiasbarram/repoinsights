from datetime import datetime
from typing import Union
from ..comment import GHCommitComment
from ..commit import GHCommit
from github.Repository import Repository


class CommitHandler:
    def __init__(self, repo: Repository):
        self.repo = repo

    def get_commits(self, since: Union[None, datetime], until: Union[None, datetime]):
        kwargs = {}
        if since:
            kwargs["since"] = since
        if until:
            kwargs["until"] = until

        commits = self.repo.get_commits(**kwargs)
        return [GHCommit(commit) for commit in commits]

    def get_commit_comments(self, commit_sha: str):
        comments = self.repo.get_commit(commit_sha).get_comments()
        return [GHCommitComment(comment) for comment in comments]

    def get_commit_parents(self, commit_sha: str):
        parents = self.repo.get_commit(commit_sha).parents
        return [GHCommit(parent) for parent in parents]
