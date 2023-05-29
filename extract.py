from datetime import datetime
import argparse
from loguru import logger

from services.extract_service.client import InsightsClient
from services.extract_service.excepctions.exceptions import (
    GitHubUserException,
    ProjectNotFoundError,
)


class Logger:
    def __init__(self, debug):
        self.debug = debug

    def setup(self):
        if not self.debug:
            logger.remove()
            dt = datetime.now()
            dt_str = dt.strftime("%Y-%m-%dT%H:%M:%S")
            logger.add(f"logs/extract-{dt_str}.log", backtrace=True, diagnose=True)


def handle_extract_exceptions(client, e):
    if isinstance(e, GitHubUserException):
        logger.error("Repositorio encontrado con otro nombre, encolando para eliminar")
        client.enqueue_to_modificacion(type="rename")
    elif isinstance(e, ProjectNotFoundError):
        logger.error("Proyecto no encontrado, marcar como eliminado")
    elif isinstance(e, KeyboardInterrupt):
        logger.error("Proceso interrumpido por el usuario")
        client.enqueue_to_pendientes()
    else:
        logger.error(f"Fallo en la extracción. volviendo a encolar: {e}")
        client.enqueue_to_pendientes()


def handle_load_exceptions(client, e):
    logger.error(f"Fallo en la carga. volviendo a encolar: {e}")
    client.enqueue_to_pendientes("load")


def main(debug=None):
    """
    "commits", "pull_requests", "issues", "labels", "stargazers", "members", "milestones
    """
    logger = Logger(debug)
    logger.setup()

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
    except Exception as e:
        handle_extract_exceptions(client, e)
        return

    try:
        client.load(results)
    except Exception as e:
        handle_load_exceptions(client, e)
        return

    client.enqueue_to_curado()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="InsightsClient script")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    while True:
        main(args.debug)