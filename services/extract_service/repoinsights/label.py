from typing import Union
from github import Label, Issue, Project


class InsightsLabel:
    def __init__(self, label):
        self.name = label["name"]
        self.color = label["color"]
        self.description = label["description"]

    def set_project_id(self, repo_id: Union[int, None]):
        self.repo_id = repo_id

    def to_dict(self):
        return {"repo_id": self.repo_id, "name": self.name}
