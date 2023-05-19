from services.traspaso_service.queue_client import QueueClient
from services.traspaso_service.db_connector.connector import DBConnector
from services.traspaso_service.db_connector.database_handler import DatabaseHandler
from services.traspaso_service.db_connector.models import Project, User, Commit
from services.traspaso_service.utils.utils import gh_api_to_datetime
from loguru import logger
from typing import Dict, Any, List, Tuple, Union
from services.traspaso_service.traspaso.traspaso import Client as TraspasoClient
import json


class UUIDNotFoundException(Exception):
    pass


def handle_failed_project(
    project: Dict, queue_client: QueueClient, failed_projects: List[Dict[str, Any]]
):
    logger.error("Error al traspasar el proyecto {project}", project=project)
    json_data = json.dumps(project)
    queue_client.enqueue(json_data)
    failed_projects.append(project)


def all_done(failed: List[Dict[str, Any]], saved: List[Dict[str, Any]]):
    logger.warning(
        "Todos los proyectos ya han sido traspasados \t fallidos {failed_projects} \t exitosos {saved_projects}",
        failed_projects=len(failed),
        saved_projects=len(saved),
    )


def main(uuids):
    saved_projects = []
    failed_projects = []
    queue_client = QueueClient()
    project = queue_client.get_from_queue_curado()

    db_handler = DatabaseHandler(DBConnector())
    if project.get("uuid") is None:
        raise UUIDNotFoundException("No se ha podido obtener el uuid del proyecto")

    uuid = project["uuid"]
    logger.info("Traspasando proyecto {project}", project=project)
    traspaso_client = TraspasoClient(db_handler, uuid)
    if uuid in uuids:
        all_done(
            failed=failed_projects,
            saved=saved_projects,
        )
        exit(0)
    # flag the first uuid in the queue.
    uuids.append(uuid)
    try:
        traspaso_client.migrate()
        saved_projects.append(project)

    except Exception as e:
        logger.error(e)
        handle_failed_project(project, queue_client, failed_projects)


if __name__ == "__main__":
    uuids = []
    while True:
        main(uuids)
