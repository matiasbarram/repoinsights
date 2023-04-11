from typing import Union
from github import Label, Issue, Project
from .repository import GHRepository


class GHLabel(GHRepository):
    def get_issue_labels(self, issue: Issue.Issue):
        labels = issue.get_labels()
        return labels

    def get_project_labels(self):
        labels = self.repo.get_labels()
        return labels

    def get_label_data(self, label: Label.Label):
        data = {
            "repo_id": self.repo.id,
            "name": label.name,
        }
        print(f"label data {data}")
        return data
