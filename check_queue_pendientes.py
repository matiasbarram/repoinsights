from services.check_update_service.connector import DBConnector
from services.check_update_service.database_handler import DatabaseHandler
import pika
import json
import os
from typing import Dict, Any
from loguru import logger


class QueueClient:
    def connect(self):
        self.rabbit_user = os.environ["RABBIT_USER"]
        self.rabbit_pass = os.environ["RABBIT_PASS"]
        self.rabbit_host = os.environ["RABBIT_HOST"]
        credentials = pika.PlainCredentials(self.rabbit_user, self.rabbit_pass)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.rabbit_host, credentials=credentials)
        )
        self.channel = connection.channel()
        self.channel.queue_declare(queue="pendientes")

    def enqueue(self, project: Dict[str, Any]):
        project_json = json.dumps(project, default=str)
        self.channel.basic_publish(
            exchange="", routing_key="pendientes", body=project_json
        )
        logger.info("Enqueued project {project}", project=project_json)


connector = DBConnector()
db_handler = DatabaseHandler(connector)
queue_client = QueueClient()
queue_client.connect()
projects = db_handler.get_updated_projects()
for project in projects:
    queue_client.enqueue(project)
