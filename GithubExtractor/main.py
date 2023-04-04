from github import (
    Github,
    Repository,
)
from .GHIssue import GHIssue
from .GHCommit import GHCommit
from .GHPullRequest import GHPullRequest
from .GHUser import GHUser
from .GHLabel import GHLabel
from .GHGetToken import GHGetToken


class GHExtractor(GHIssue, GHCommit, GHPullRequest, GHUser, GHLabel):
    def __init__(self, gh_user: GHGetToken, gh_repo: str) -> None:
        self.connector: Github = gh_user.connector
        self.repo: Repository.Repository = self.connector.get_repo(gh_repo)

    def get_project_owner(self):
        owner = self.repo.owner
        return owner

    def get_watchers(self):
        watchers = self.repo.get_watchers()
        return watchers

    def get_members(self):
        members = self.repo.get_collaborators()
        return members
