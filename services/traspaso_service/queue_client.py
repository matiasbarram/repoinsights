import pika
import os
from loguru import logger
import json
from typing import Dict, Any, Union, Optional


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

    def get_from_queue_curado(self) -> Dict[str, Any]:
        self.channel.queue_declare(queue=self.queue_curado, durable=True)
        method_frame, _, body = self.channel.basic_get(self.queue_curado)
        if method_frame is None:
            logger.warning("No hay proyectos en la cola")
            exit(0)

        self.channel.basic_ack(method_frame.delivery_tag) if method_frame else None
        data = body.decode("utf-8")
        project = json.loads(data)
        if project is None:
            logger.warning("No hay proyectos en la cola")
            exit(0)
        return project

    def enqueue(self, project: str):
        self.channel.queue_declare(queue=self.queue_curado, durable=True)
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_curado,
            body=project,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
        )
        logger.info(f"Project {project} published")
