from typing import Union
from github import Label, Issue, Project


class InsightsLabel:
    def __init__(self, label):
        self.name = label.name
        self.color = label.color
        self.description = label.description

    def to_dict(self):
        return {
            "name": self.name,
            "color": self.color,
            "description": self.description,
        }
