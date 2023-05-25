from datetime import datetime
from loguru import logger
import argparse
from pprint import pprint
import json
import os

from services.extract_service.client import InsightsClient
from services.extract_service.excepctions.exceptions import (
    GitHubUserException,
    ProjectNotFoundError,
)


class Logger:
    def __init__(self, debug):
        self.debug = debug

    def logs(self):
        if not self.debug:
            logger.remove()
            dt = datetime.now()
            dt_str = dt.strftime("%Y-%m-%dT%H:%M:%S")
            logger.add(f"logs/extract-{dt_str}.log", backtrace=True, diagnose=True)


def main(debug=None):
    """
    "commits", "pull_requests", "issues", "labels", "stargazers", "members", "milestones
    """
    logs = Logger(debug)
    logs.logs()
    data_types = [
        "commits",
        "pull_requests",
        "issues",
        "labels",
        "milestones",
    ]

    client = InsightsClient(data_types)
    try:
        results = client.extract()
        client.load(results)
        client.enqueue_to_curado()

    except GitHubUserException as e:
        logger.error("Repositorio migrado, encolando para eliminar")
        # todo encolar para eliminar

    except ProjectNotFoundError as e:
        logger.error("Proyecto no encontrado, marcar como eliminado")
        client.enqueue_to_modificacion(type="rename")

    except KeyboardInterrupt:
        logger.error("Proceso interrumpido por el usuario")
        client.enqueue_to_pendientes()

    except Exception as e:
        logger.error(f"Fallo en la extracción. volviendo a encolar: {e}")
        client.enqueue_to_pendientes()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="InsightsClient script")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    main(args.debug)
