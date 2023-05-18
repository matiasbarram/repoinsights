import pika
import os
from loguru import logger
import json
from typing import Dict, Any, Union


class QueueClient:
    def __init__(self):
        self.user = os.environ["RABBIT_USER"]
        self.password = os.environ["RABBIT_PASS"]
        self.host = os.environ["RABBIT_HOST"]
        self.queue_curado = os.environ["RABBIT_QUEUE_CURADO"]
        self.queue_pendientes = os.environ["RABBIT_QUEUE_PENDIENTES"]
        self.credentials = pika.PlainCredentials(self.user, self.password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, credentials=self.credentials)
        )
        self.channel = self.connection.channel()

    def get_from_queue(self) -> Union[Dict[str, Any], None]:
        self.channel.queue_declare(queue=self.queue_pendientes, durable=True)
        method_frame, _, body = self.channel.basic_get(self.queue_pendientes)
        if method_frame:
            self.channel.basic_ack(method_frame.delivery_tag)
            data = body.decode("utf-8")
            return json.loads(data)
        else:
            logger.info("No hay proyectos en la cola")
            exit(0)

    def check_queue(self, name):
        if name == "pendientes":
            queue = self.queue_pendientes
        elif name == "curado":
            queue = self.queue_curado
        else:
            raise ValueError("Invalid queue name")
        return queue

    def enqueue(self, project: str, client_queue: str):
        queue = self.check_queue(client_queue)
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_curado,
            body=project,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
        )
        logger.info(f"Project {project} published")
