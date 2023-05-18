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


class Client:
    def __init__(self, db: DatabaseHandler, project: Dict[str, Any]):
        self.db = db
        self.uuid = project["uuid"]
        self.last_extraction = gh_api_to_datetime(project["until"])
        self.owner = project["owner"]


def main():
    queue_client = QueueClient()
    project = queue_client.get_from_queue_curado()
    if project is None:
        logger.warning("No hay proyectos en la cola")
        exit(0)

    db_handler = DatabaseHandler(DBConnector())
    if project.get("uuid") is None:
        raise UUIDNotFoundException("No se ha podido obtener el uuid del proyecto")

    uuid = project["uuid"]
    logger.info("Traspasando proyecto {project}", project=project)
    traspaso_client = TraspasoClient(db_handler, uuid)
    try:
        traspaso_client.migrate()
    except Exception as e:
        logger.error("Error al traspasar el proyecto {project}", project=project)
        logger.error(e)
        json_data = json.dumps(project)
        queue_client.enqueue(json_data)
        exit(1)


if __name__ == "__main__":
    main()
