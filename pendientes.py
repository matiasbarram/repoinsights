import json
import os
from typing import Dict, Any
from loguru import logger
import pika
from services.pendientes_service.connector import DBConnector
from services.pendientes_service.database_handler import DatabaseHandler


class RabbitMQError(Exception):
    """
    Handle all rabbitmq errors
    """


class QueueConnector:
    """
    Clase que se conecta con rabbitmq y lee y crea los elementos en la cola
    """

    def __init__(self) -> None:
        self.rabbit_user = os.environ["RABBIT_USER"]
        self.rabbit_pass = os.environ["RABBIT_PASS"]
        self.rabbit_host = os.environ["RABBIT_HOST"]
        self.channel = None

    def connect(self):
        """
        Crear o accede a una rabbitmq
        """
        credentials = pika.PlainCredentials(self.rabbit_user, self.rabbit_pass)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.rabbit_host, credentials=credentials)
        )
        self.channel = connection.channel()
        self.channel.queue_declare(queue="pendientes", durable=True)

    def enqueue(self, project: Dict[str, Any]):
        """
        Agrega a la cola de pendientes un proyecto obtenido desde consolidada
        """
        project_json = json.dumps(project, default=str)
        if self.channel is None:
            raise RabbitMQError("Channel not found")

        self.channel.basic_publish(
            exchange="",
            routing_key="pendientes",
            body=project_json,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
            mandatory=True,
        )
        logger.info("Enqueued project {project}", project=project_json)


def main():
    """
    Almacena en cola todos los proyectos que no han sido actualizados.
    """
    connector = DBConnector()
    db_handler = DatabaseHandler(connector)
    queue_client = QueueConnector()
    queue_client.connect()
    projects = db_handler.get_updated_projects()
    for project in projects:
        queue_client.enqueue(project)


if __name__ == "__main__":
    import sys

    sys.stdout.flush()
    main()
