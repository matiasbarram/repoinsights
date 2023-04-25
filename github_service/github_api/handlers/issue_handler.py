from ..isssue import GHIssue
from ..milestone import GHMilestone
from ..issue_event import GHIssueEvent
from ..comment import GHIssueComment
from github.Issue import Issue
from datetime import datetime
from pprint import pprint
from typing import Union, List, Any, Dict
from ...requests.github import GitHubExtractor
import json


class IssueHandler:
    def __init__(self, repo: GitHubExtractor):
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
        kwargs: Dict[str, Any] = {"state": state}
        if start_date:
            kwargs["since"] = start_date
        if end_date:
            kwargs["until"] = end_date
        issues = self.repo.obtener_issues(**kwargs)
        return [GHIssue(issue) for issue in issues if not issue.get("pull_request")]

    def set_labels(self, issue_objects: list, issues):
        issue_obj: GHIssue
        issue: Issue
        for issue_obj, issue in zip(issue_objects, issues):
            issue_obj.set_labels(issue.labels)

    # def get_milestones(self, state="all"):
    #     milestones = self.repo.get_milestones(state=state)
    #     milestone_objects = [GHMilestone(milestone) for milestone in milestones]
    #     return milestone_objects

    # # ARREGLAR NO DEBERIAN LLAMAR A LA API DEBERIA HACERSE DE UNA MEJOR MANERA

    # def get_issue_comments(self, issue):
    #     comments = self.repo.get_issue(issue.number).get_comments()
    #     return [GHIssueComment(comment) for comment in comments]

    # def get_issue_events(self, issue: GHIssue):
    #     events = self.repo.get_issue(issue.issue_id).get_events()
    #     return [GHIssueEvent(event) for event in events]
