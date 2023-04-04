from github import Github
from .GHToken import GHToken
from pprint import pprint


class CurateMetrics:
    def __init__(self, project) -> None:
        self.core_contributors_min = 2

        self.token = GHToken().get_token()
        self.gh = Github(self.token)
        self.repo = self.gh.get_repo(project)

    def get_contributors_data(self, contributors, total_commits):
        contributors_data = []
        for contributor in contributors:
            contributor_percentage = contributor.contributions / total_commits * 100
            contributors_data.append(
                {
                    "id": contributor.id,
                    "login": contributor.login,
                    "total": contributor.contributions,
                    "percentage": contributor_percentage,
                }
            )

        return contributors_data

    def calc_core_contributors(self, contributors: list[dict]):
        core_contributors = []
        sum_percentage = 0
        index = 0
        while index < len(contributors) and sum_percentage < 80.0:
            contributor = contributors[index]
            core_contributors.append(contributor)
            sum_percentage += contributor["percentage"]
            index += 1
        return {
            "core_contributors": core_contributors,
            "cardinality": len(core_contributors),
        }

    """
    Core contributors: is the cardinality of the smallest set of contributors whose total number of commits 
    to a source code repository
    accounts for 80% or more of the total contributions
    que endpoints de la api de github debo utilizar
    """

    def core_contributors_metrics(self) -> None:
        contributors = self.repo.get_contributors()
        total_commits = self.repo.get_commits().totalCount
        contributors_data = self.get_contributors_data(contributors, total_commits)
        core_contributors = self.calc_core_contributors(contributors_data)
        pprint(core_contributors)
