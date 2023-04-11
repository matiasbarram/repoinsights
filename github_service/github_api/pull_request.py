from github.PullRequest import PullRequest
from .comment import GHPullRequestComment


class GHPullRequest:
    def __init__(self, pull_request: PullRequest):
        self.number = pull_request.number
        self.title = pull_request.title
        self.description = pull_request.body
        self.state = pull_request.state
        self.created_at = pull_request.created_at
        self.updated_at = pull_request.updated_at
        self.closed_at = pull_request.closed_at
        self.merged_at = pull_request.merged_at
        self.author = pull_request.user.login
        self.base_branch = pull_request.base.ref
        self.head_branch = pull_request.head.ref
        self.body = pull_request.body
        self.raw_pull_request = pull_request

    def __str__(self):
        return f"Pull Request #{self.number} ({self.state})"

    def set_comments(self, comments: list[GHPullRequestComment]):
        self.comments = comments

    def get_comments(self):
        comments = self.raw_pull_request.get_comments()
        return [GHPullRequestComment(comment) for comment in comments]

    def to_dict(self):
        return {
            "number": self.number,
            "title": self.title,
            "body": self.body,
            "state": self.state,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "closed_at": self.closed_at,
            "merged_at": self.merged_at,
            "author": self.author,
        }
