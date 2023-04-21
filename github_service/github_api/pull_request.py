from github.PullRequest import PullRequest
from github.Commit import Commit
from .comment import GHPullRequestComment
from .repository import GHRepository
from .commit import GHCommit
from .user import GHUser


class GHPullRequest:
    def __init__(self, pull_request: PullRequest):
        self.number = pull_request.number
        self.title = pull_request.title
        self.description = pull_request.body
        self.state = pull_request.state
        self.created_at = pull_request.created_at
        self.updated_at = pull_request.updated_at
        self.closed_at = pull_request.closed_at
        self.merged = True if pull_request.merged_at else False
        self.base_branch = pull_request.base.ref
        self.head_branch = pull_request.head.ref
        self.base_commit_sha = pull_request.base.sha
        self.head_commit_sha = pull_request.head.sha
        self.body = pull_request.body
        self.author = GHUser(pull_request.user)
        self.base_repo = GHRepository(pull_request.base.repo)
        self.head_repo = GHRepository(pull_request.head.repo)
        self.intra_branch = True if self.base_repo == self.head_repo else False
        self.raw_pull_request = pull_request

    def __str__(self):
        return f"Pull Request #{self.number} ({self.state})"

    def set_head_commit(self, commit: GHCommit):
        self.head_commit = commit

    def set_base_commit(self, commit: GHCommit):
        self.base_commit = commit

    def set_head_commit_id(self, commit_id: int):
        self.head_commit_id = commit_id

    def set_base_commit_id(self, commit_id: int):
        self.base_commit_id = commit_id

    def set_head_repo_id(self, repo_id: int):
        self.head_repo_id = repo_id

    def set_base_repo_id(self, repo_id: int):
        self.base_repo_id = repo_id

    def set_comments(self, comments: list[GHPullRequestComment]):
        self.comments = comments

    def set_user_id(self, user_id: int):
        self.user_id = user_id

    def set_project_id(self, project_id: int):
        self.project_id = project_id

    def get_comments(self):
        comments = self.raw_pull_request.get_comments()
        return [GHPullRequestComment(comment) for comment in comments]

    # def to_dict(self):
    #     return {
    #         "head_repo_id": self.head_repo.id,
    #         "base_repo_id": self.base_repo.id,
    #         "head_commit": self.head_commit_id,
    #         "base_commit": self.base_commit_id,
    #         "user_id": self.author.login,
    #         "pullreq_id": self.number,
    #         "intra_branch": self.intra_branch,
    #         "merged": self.merged,
    #     }
