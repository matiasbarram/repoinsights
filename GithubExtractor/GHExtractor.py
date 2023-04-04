from github import Github, Repository, Milestone
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

    def get_issues(self):
        issues = self.repo.get_issues(state="all", sort="created")
        return issues

    def get_milestones(self):
        milestones = self.repo.get_milestones(state="all")
        return milestones

    def get_milestone_data(self, milestone: Milestone.Milestone):
        data = {
            "id": milestone.id,
            "repo_id": self.repo.id,  # GET FROM DB
            "name": milestone.title,
        }
        print(f"Milestone data {data}")
        return data
