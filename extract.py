from extract_service.clients.client import InsightsClient

from datetime import datetime
from pprint import pprint
import json
from loguru import logger


def main():
    owner = "gousiosg"
    repo = "github-mirror"
    since = datetime(2019, 1, 10)
    until = datetime(2022, 2, 20)
    # since = None
    # until = None
    data_types = [
        "commits",
        "pull_requests",
        "issues",
        # "labels",
        # "stargazers",
        # "members",
        # "milestones",
    ]

    client = InsightsClient(owner, repo, since, until, data_types)
    results = client.extract()
    client.load(results)
    client.enqueue()


if __name__ == "__main__":
    main()
