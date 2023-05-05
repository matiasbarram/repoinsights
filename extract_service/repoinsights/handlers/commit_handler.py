from typing import Union, List
from extract_service.repoinsights.commit import InsightsCommit
from extract_service.repoinsights.comment import InsightsCommitComment
from extract_service.github_api.extractor import GitHubExtractor
from datetime import datetime


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

    def get_commit_comments(self, commits: List[InsightsCommit]):
        comments = self.repo.obtener_comments()
        for commit in commits:
            # find commit.id in comments list
            commit_comments = [
                InsightsCommitComment(comment)
                for comment in comments
                if comment["commit_id"] == commit.sha
            ]
            commit.set_comments(commit_comments)

    # def get_commit_parents(self, commit_sha: str):
    #     parents = self.repo.get_commit(commit_sha).parents
    #     return [GHCommit(parent) for parent in parents]
