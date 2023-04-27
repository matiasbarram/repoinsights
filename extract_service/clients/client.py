from .extract_client import ExtractDataClient
from .load_client import LoadDataClient


class InsightsClient:
    def __init__(self, owner, repo, since, until, data_types) -> None:
        self.owner = owner
        self.repo = repo
        self.since = since
        self.until = until
        self.data_types = data_types

        self.extract_data = ExtractDataClient(
            owner=self.owner,
            repo=self.repo,
            since=self.since,
            until=self.until,
            data_types=self.data_types,
        )

    def extract(self):
        return self.extract_data.extract()

    def load(self, results):
        return LoadDataClient(results).load_data()

    def enqueue(self):
        pass
