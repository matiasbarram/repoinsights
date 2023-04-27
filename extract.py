from extract_service.clients.client import InsightsClient


from datetime import datetime
from pprint import pprint
import json
from loguru import logger


def main():
    data_types = [
        "commits",
        "pull_requests",
        "issues",
        # "labels",
        # "stargazers",
        # "members",
        # "milestones",
    ]

    client = InsightsClient(data_types)
    while True:
        client.get_from_pendientes()
        results = client.extract()
        client.load(results)
        client.enqueue_to_curado()


if __name__ == "__main__":
    main()
