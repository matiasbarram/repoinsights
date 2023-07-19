from datetime import datetime
import argparse
from loguru import logger

from services.extract_service.client import InsightsClient
from services.extract_service.excepctions.exceptions import (
    GitHubUserException,
    ProjectNotFoundError,
    LimitExceededError,
    EmptyQueueError,
)
from time import sleep


class Logger:
    def __init__(self, debug):
        self.debug = debug

    def setup(self):
        if not self.debug:
            logger.remove()
        dt = datetime.now()
        dt_str = dt.strftime("%Y-%m-%dT%H:%M:%S")
        logger.add(f"logs/extract-{dt_str}.log", backtrace=True, diagnose=True)


def handle_extract_exceptions(client: InsightsClient, e):
    if isinstance(e, GitHubUserException):
        client.enqueue_to_modificacion(
            action_type="rename", new={"owner": "new_name", "repo": "new_name"}
        )
        logger.exception(
            "Repositorio encontrado con otro nombre, encolando para eliminar",
            traceback=True,
        )
    elif isinstance(e, ProjectNotFoundError):
        client.enqueue_to_modificacion(action_type="delete")
        logger.exception(
            "Proyecto no encontrado, marcar como eliminado", traceback=True
        )

    elif isinstance(e, KeyboardInterrupt):
        logger.exception("Proceso interrumpido por el usuario", traceback=True)
        client.enqueue_to_pendientes()

    elif isinstance(e, LimitExceededError):
        logger.exception(
            "Se superó el límite de intentos, encolando para pendientes", traceback=True
        )
        client.enqueue_to_failed()
    elif isinstance(e, EmptyQueueError):
        logger.info("No hay proyectos en la cola", traceback=False)

    else:
        logger.exception(
            f"Fallo en la extracción. volviendo a encolar: {e}", traceback=True
        )
        client.enqueue_to_pendientes()


def handle_load_exceptions(client: InsightsClient, e):
    logger.exception(f"Fallo en la carga. volviendo a encolar: {e}", traceback=True)
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
        client.get_from_pendientes()

        if client.attempt > 2:
            raise LimitExceededError("Se superó el límite de intentos")

        results = client.extract()
        client.load(results)
        client.enqueue_to_curado()

    except Exception as e:
        handle_extract_exceptions(client, e)
        return


if __name__ == "__main__":
    while True:
        parser = argparse.ArgumentParser(description="InsightsClient script")
        parser.add_argument("--debug", action="store_true", help="Enable debug mode")
        parser.add_argument(
            "--single",
            action="store_true",
            help="Run only one time and exit",
        )
        args = parser.parse_args()
        main(args.debug)
        print("Sleeping for 60 seconds")
        sleep(60)
        if args.single:
            break
