from github import Github
from .GHToken import GHToken
from pprint import pprint
from .CoreContributors import CoreContributors


class CurateMetrics:
    def __init__(self, project) -> None:
        self.core_contributors_min = 2

        self.token = GHToken().get_token()
        self.gh = Github(self.token)
        self.repo = self.gh.get_repo(project)

    def core_contributors_metric(self):
        core_contributors = CoreContributors(self.repo)
        return core_contributors.calc()
