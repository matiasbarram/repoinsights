from services.traspaso_service.queue_client import QueueClient
from services.traspaso_service.db_connector.connector import DBConnector
from services.traspaso_service.db_connector.database_handler import DatabaseHandler
from services.traspaso_service.db_connector.models import Project, User, Commit
from services.traspaso_service.utils.utils import gh_api_to_datetime
from loguru import logger
from typing import Dict, Any, List, Tuple, Union
from services.traspaso_service.traspaso import Client as TraspasoClient


class EmptyQueueException(Exception):
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
        raise EmptyQueueException("No hay proyectos en la cola")

    db_handler = DatabaseHandler(DBConnector())
    uuid = project["uuid"]
    logger.info("Traspasando proyecto {project}", project=project)
    traspaso_client = TraspasoClient(db_handler, uuid)
    traspaso_client.migrate()


if __name__ == "__main__":
    main()
