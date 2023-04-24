from github.Repository import Repository
from ..isssue import GHIssue
from ..milestone import GHMilestone
from ..issue_event import GHIssueEvent
from ..comment import GHIssueComment
from github.Issue import Issue
from datetime import datetime
from pprint import pprint
from typing import Union, List

# from label import GHLabel


class IssueHandler:
    def __init__(self, repo: Repository):
        self.repo = repo

    def _get_filtered_issues(self, issues):
        print("Getting GHIssues")
        issue_objects = [GHIssue(issue) for issue in issues if not issue.pull_request]
        self.set_labels(issue_objects, issues)
        return issue_objects

    def get_issues(
        self,
        state="all",
        start_date: Union[datetime, None] = None,
        end_date: Union[datetime, None] = None,
    ):
        if start_date and end_date:
            return self.get_issues_between_dates(start_date, end_date, state)

        kwargs = {"state": state}
        issues: List[GHIssue] = []
        page_number = 0
        while True:
            paginated_issues = self.repo.get_issues(**kwargs).get_page(page_number)
            if not paginated_issues:
                break
            filtered_issues = self._get_filtered_issues(paginated_issues)
            issues.extend(filtered_issues)

            if len(paginated_issues) < 100:
                break
            page_number += 1

        return issues

    def get_issues_between_dates(
        self, start_date: datetime, end_date: datetime, state="all"
    ):
        kwargs = {"state": state}
        if start_date:
            kwargs["since"] = start_date  # type: ignore

        issues: list[GHIssue] = []
        pag = 0
        while True:
            issues_per_page = self.repo.get_issues(
                **kwargs, sort="created", direction="desc"
            ).get_page(pag)
            if not issues_per_page:
                break
            issue: Issue
            for issue in issues_per_page:
                if issue.created_at > end_date or issue.created_at < start_date:
                    continue
                issues.append(GHIssue(issue))
            pag += 1

        return issues

    def set_labels(self, issue_objects: list, issues):
        issue_obj: GHIssue
        issue: Issue
        for issue_obj, issue in zip(issue_objects, issues):
            issue_obj.set_labels(issue.labels)

    def get_milestones(self, state="all"):
        milestones = self.repo.get_milestones(state=state)
        milestone_objects = [GHMilestone(milestone) for milestone in milestones]
        return milestone_objects

    # ARREGLAR NO DEBERIAN LLAMAR A LA API DEBERIA HACERSE DE UNA MEJOR MANERA

    def get_issue_comments(self, issue):
        comments = self.repo.get_issue(issue.number).get_comments()
        return [GHIssueComment(comment) for comment in comments]

    def get_issue_events(self, issue: GHIssue):
        events = self.repo.get_issue(issue.issue_id).get_events()
        return [GHIssueEvent(event) for event in events]
