from typing import Dict, Any, List, Tuple, Union
from loguru import logger
import json
from time import sleep
from services.traspaso_service.queue_client import QueueClient
from services.traspaso_service.db_connector.connector import DBConnector
from services.traspaso_service.db_connector.database_handler import DatabaseHandler
from services.traspaso_service.db_connector.models import Project, User, Commit
from services.traspaso_service.traspaso.traspaso import Client as TraspasoClient
from services.metrics_service.calc import calculate_metrics
import pika
import pika.exceptions
import os
import json
from services.traspaso_service.queue_client import QueueClient


class UUIDNotFoundException(Exception):
    pass


def add_to_queue(
    project: Dict,
    queue_client: QueueClient,
):
    logger.error("Error al traspasar el proyecto {project}", project=project)
    json_data = json.dumps(project)
    queue_client.enqueue(json_data)


def enqueue_to_modificacion(
    queue_client: QueueClient, project: Dict, action_type, **kwargs
):
    project_data = {}
    if action_type not in ["rename", "delete", "transfer"]:
        raise ValueError('Invalid action_type. Must be either "rename" or "delete"')

    project_data["action"] = action_type
    project_data["project"] = {"owner": project["owner"], "repo": project["repo"]}

    if action_type == "rename":
        new = kwargs.get("new")
        if not new:
            raise BaseException("No se especificó el nuevo nombre del proyecto")
        project_data["new"] = {"owner": new["owner"], "repo": new["repo"]}

    json_data = json.dumps(project_data)
    queue_client.enqueue(json_data, "modificaciones")


def all_done(failed: List[Dict[str, Any]], saved: List[Dict[str, Any]]):
    logger.warning(
        "Todos los proyectos ya han sido traspasados \t fallidos {failed_projects} \t exitosos {saved_projects}",
        failed_projects=len(failed),
        saved_projects=len(saved),
    )


class TraspasoListener:
    def __init__(self):
        self.user = os.environ["RABBIT_USER"]
        self.password = os.environ["RABBIT_PASS"]
        self.host = os.environ["RABBIT_HOST"]
        self.queue_curado = os.environ["RABBIT_QUEUE_CURADO"]
        self.credentials = pika.PlainCredentials(self.user, self.password)
        self.db_handler = DatabaseHandler(DBConnector())
        self.queue_client = QueueClient()

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, credentials=self.credentials)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_curado, durable=True)
        self.channel.basic_consume(
            queue=self.queue_curado, on_message_callback=self.callback, auto_ack=True
        )

    def callback(self, ch, method, properties, body):
        project = json.loads(body)
        uuid = project["uuid"]
        logger.info("Traspasando proyecto {project}", project=project)
        traspaso_client = TraspasoClient(self.db_handler, uuid)
        try:
            traspaso_client.migrate()
            calculate_metrics(project["repo"], project["uuid"])
            logger.info("Proyecto traspasado exitosamente {project}", project=project)
        except Exception as e:
            logger.exception("Error", traceback=True)
            enqueue_to_modificacion(self.queue_client, project, "delete")
            ch.basic_ack(
                delivery_tag=method.delivery_tag
            )  # Confirm the message as processed
            logger.error(
                "Error al traspasar el proyecto {project}",
                project=project,
                exc_info=True,
            )

    def start_listening(self):
        while True:
            try:
                print(" [*] Waiting for messages. To exit press CTRL+C")
                self.channel.start_consuming()
            except pika.exceptions.StreamLostError:
                logger.error("Connection lost. Trying to reconnect in 10 seconds...")
                sleep(10)
                self.connect()
            except Exception as e:
                logger.error(f"Unexpected error: {e}. Retrying in 10 seconds...")
                sleep(10)


if __name__ == "__main__":
    listener = TraspasoListener()
    listener.connect()
    listener.start_listening()
