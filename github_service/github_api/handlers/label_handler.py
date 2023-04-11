from github.Repository import Repository
from ..label import GHLabel


class LabelHandler:
    def __init__(self, repo: Repository):
        self.repo = repo

    def get_labels(self):
        labels = self.repo.get_labels()
        print(f"Total labels {labels.totalCount}")
        return [GHLabel(label) for label in labels]
