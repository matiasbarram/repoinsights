from typing import Union
from github import Label, Issue, Project


class GHLabel:
    def get_labels(self, entity: Union[Issue.Issue, Project.Project]):
        labels = entity.get_labels()
        return labels

    def get_label_data(self, label: Label.Label):
        data = {
            "repo_id": self.repo.id,
            "name": label.name,
        }
        print(f"label data {data}")
        return data
