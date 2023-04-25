from ..config import GHToken
from .repository import InsightsRepository
from .handlers.commit_handler import InsightsCommitHandler
from .handlers.project_user_handler import InsightsProjectUserHandler
from .handlers.label_handler import InsightsLabelHandler
from .handlers.issue_handler import InsightsIssueHandler
from .handlers.pull_request_handler import InsightsPullRequestHandler

from ..github_api.github import GitHubExtractor


class InsightsClient:
    def __init__(self, owner: str, repo: str):
        tokens = GHToken().get_public_tokens()
        tokens_iter = iter(tokens)

        self.repo = GitHubExtractor(owner, repo, tokens_iter)

        if self.repo.repositorio is None:
            raise Exception("Repository not found")
        self.repository = InsightsRepository(self.repo.repo)

        self.commit_handler = InsightsCommitHandler(self.repo)
        self.project_handler = InsightsProjectUserHandler(self.repo)
        self.pull_request_handler = InsightsPullRequestHandler(self.repo)
        self.user_handler = ()
        self.label_handler = InsightsLabelHandler(self.repo)
        self.issue_handler = InsightsIssueHandler(self.repo)
