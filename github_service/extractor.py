from github import Github, Repository, Milestone
from .github_api.isssue import GHIssue
from .github_api.commit import GHCommit
from .github_api.pull_request import GHPullRequest
from .github_api.user import GHUser
from .github_api.label import GHLabel


class GHExtractor(GHIssue, GHCommit, GHPullRequest, GHUser, GHLabel):
    def get_project_owner(self):
        owner = self.repo.owner
        return owner

    def get_watchers(self):
        watchers = self.repo.get_watchers()
        return watchers

    def get_members(self):
        members = self.repo.get_contributors()
        return members

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
