from datetime import datetime
import argparse
import json
from time import sleep
from loguru import logger

from services.extract_service.client import InsightsClient
from services.extract_service.utils.utils import api_date
from services.extract_service.queue_module.enqueue_client import QueueController


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
    else:
        logger.exception(
            f"Fallo en la extracción. volviendo a encolar: {e}", traceback=True
        )
        client.enqueue_to_pendientes()


def handle_load_exceptions(client, e):
    logger.exception(f"Fallo en la carga. volviendo a encolar: {e}", traceback=True)
    client.enqueue_to_pendientes("load")


import pika
import pika.exceptions
import os
import json
from time import sleep
from services.extract_service.client import InsightsClient


class ExtractListener:
    def __init__(self):
        self.user = os.environ["RABBIT_USER"]
        self.password = os.environ["RABBIT_PASS"]
        self.host = os.environ["RABBIT_HOST"]
        self.queue_pendientes = os.environ["RABBIT_QUEUE_PENDIENTES"]
        self.credentials = pika.PlainCredentials(self.user, self.password)

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, credentials=self.credentials)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_pendientes, durable=True)
        self.channel.basic_consume(
            queue=self.queue_pendientes,
            on_message_callback=self.callback,
            auto_ack=True,
        )

    def callback(self, ch, method, properties, body):
        project = json.loads(body)
        data_types = ["commits", "pull_requests", "issues", "labels", "milestones"]
        client = InsightsClient(data_types, project)
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

    def start_listening(self):
        try:
            print(" [*] Waiting for messages. To exit press CTRL+C")
            self.channel.start_consuming()
        except pika.exceptions.StreamLostError:
            print("Connection lost. Trying to reconnect in 10 seconds...")
            sleep(10)
            self.connect()
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying in 10 seconds...")
            sleep(10)


if __name__ == "__main__":
    listener = ExtractListener()
    listener.connect()
    listener.start_listening()
