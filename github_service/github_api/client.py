from ..config import GHGetToken
from .handlers.commit_handler import CommitHandler
from .handlers.project_user_handler import ProjectUserHandler
from .handlers.label_handler import LabelHandler
from .handlers.issue_handler import IssueHandler
from .handlers.user_handler import UserHandler
from .handlers.pull_request_handler import PullRequestHandler


class GitHubClient:
    def __init__(self, owner, repo):
        self.github = GHGetToken().connector
        self.repo = self.github.get_repo(f"{owner}/{repo}")
        self.commit_handler = CommitHandler(self.repo)
        self.project_handler = ProjectUserHandler(self.repo)
        self.user_handler = UserHandler()
        self.label_handler = LabelHandler(self.repo)
        self.issue_handler = IssueHandler(self.repo)
        self.pull_request_handler = PullRequestHandler(self.repo)
