from github import Github
from .GHToken import GHToken
from pprint import pprint
from .CoreContributors import CoreContributors
from .CommitFrecuency import CommitFrecuency
from datetime import datetime


class CurateMetrics:
    def __init__(self, project) -> None:
        self.core_contributors_min = 2

        self.token = GHToken().get_token()
        self.gh = Github(self.token)
        self.repo = self.gh.get_repo(project)

    """
    Core contributors: is the cardinality of the smallest set of contributors whose total number of commits 
    to a source code repository
    accounts for 80% or more of the total contributions
    que endpoints de la api de github debo utilizar
    """

    def core_contributors_metric(self):
        core_contributors = CoreContributors(self.repo)
        return core_contributors.calc()

    """
    Commit frequency: is the average number of commits per month
    ci-> is the number of commits for the months i
    m -> is the number of months between the first and last commit to the repository
    # se tomaran en cuenta los meses incluidos. 2023-01 al 2023-04 se tomaran 4 meses
    """

    def commit_frecuency_metric(self, start_date: datetime, end_date: datetime):
        commit_frecuency_period = CommitFrecuency(self.repo, start_date, end_date)
        return commit_frecuency_period.calc()
