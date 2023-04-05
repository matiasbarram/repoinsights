from github.Commit import Commit
from github.Repository import Repository
from datetime import datetime, timedelta
from pprint import pprint


class CommitFrecuency:
    def __init__(self, repo: Repository, start_month: datetime, end_month: datetime):
        self.repo = repo
        self.start_date = start_month
        self.end_date = end_month
        print({"Start date", self.start_date, "End date", self.end_date})
        self.commits = repo.get_commits(
            since=self.start_date,
            until=self.end_date,
        )

    def __get_months_between_dates(self):
        months = (
            (self.end_date.year - self.start_date.year) * 12
            + (self.end_date.month - self.start_date.month)
            + 1
        )
        return months

    def __get_first_last_days_month(self, current_month: datetime):
        first_day = current_month.replace(day=1)
        if current_month.month != 12:
            last_day = current_month.replace(
                day=current_month.day,
                month=current_month.month + 1,
            ) - timedelta(days=1)
        else:
            last_day = current_month.replace(
                day=1,
                month=1,
                year=current_month.year + 1,
            ) - timedelta(days=1)
        return first_day, last_day

    def __get_commits_per_month(self, total_months):
        print("Total months", total_months)
        commits_per_month = []
        total_commits = 0
        current_month = self.start_date
        print("Current month", current_month)
        for i in range(0, total_months):
            if i != 0:
                if current_month.month == 12:
                    current_month = current_month.replace(
                        year=current_month.year + 1, month=1
                    )
                else:
                    current_month = current_month.replace(month=current_month.month + 1)
            first_day, last_day = self.__get_first_last_days_month(current_month)
            commits_month = self.repo.get_commits(since=first_day, until=last_day)
            month_data = {
                "first_day": first_day,
                "last_day": last_day,
                "commits": commits_month.totalCount,
            }
            pprint(
                {
                    "first_day": datetime.strftime(first_day, "%Y-%m-%d"),
                    "last_day": datetime.strftime(last_day, "%Y-%m-%d"),
                    "commits": commits_month.totalCount,
                }
            )
            total_commits += commits_month.totalCount
            commits_per_month.append(month_data)
        return commits_per_month, total_commits

    def calc(self):
        m = self.__get_months_between_dates()
        commits_per_month, total_commits = self.__get_commits_per_month(m)
        pprint({"Total commits", total_commits})
        sum_ci = 0
        for ci in commits_per_month:
            sum_ci += ci["commits"]
        return sum_ci / m
