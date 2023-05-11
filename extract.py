from services.extract_service.clients.client import InsightsClient


from datetime import datetime
from pprint import pprint
import json
from loguru import logger
import argparse


def main(debug=None):
    data_types = [
        "commits",
        "pull_requests",
        "issues",
        "labels",
        # "stargazers",
        # "members",
        "milestones",
    ]

    client = InsightsClient(data_types)
    if not debug:
        logger.remove()

    dt = datetime.now()
    dt_str = dt.strftime("%Y-%m-%dT%H:%M:%S")
    logger.add(f"logs/extract-{dt_str}.log", backtrace=True, diagnose=True)

    client.get_from_pendientes()
    results = client.extract()
    client.load(results)
    client.enqueue_to_curado()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="InsightsClient script")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    main(args.debug)
