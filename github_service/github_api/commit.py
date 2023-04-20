from github.Commit import Commit
from .repository import GHRepository
from datetime import datetime
from .comment import GHCommitComment


class GHCommit:
    def __init__(self, commit: Commit):
        self.sha = commit.sha
        self.message = commit.commit.message
        self.author = commit.commit.author.name
        self.date = commit.commit.author.date
        self.parents = [parent.sha for parent in commit.parents]
        self.comments = []

    def set_comments(self, comments: list[GHCommitComment]):
        self.comments = comments

    def get_comments(self) -> list[GHCommitComment]:
        return self.comments

    def to_dict(self) -> dict:
        return {
            "sha": self.sha,
            "message": self.message,
            "author": self.author,
            "date": self.date,
            "parents": self.parents,
        }
