import pika
import os
from loguru import logger
import json
from typing import Dict, Any, Union


class QueueController:
    def __init__(self):
        self.user = os.environ["RABBIT_USER"]
        self.password = os.environ["RABBIT_PASS"]
        self.host = os.environ["RABBIT_HOST"]
        self.queue_names = [
            os.environ["RABBIT_QUEUE_CURADO"],
            os.environ["RABBIT_QUEUE_PENDIENTES"],
            os.environ["RABBIT_QUEUE_MODIFICACIONES"],
        ]
        self.credentials = pika.PlainCredentials(self.user, self.password)

    def _get_connection(self):
        return pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, credentials=self.credentials)
        )

    def get_from_queue(self, queue="pendientes") -> Union[Dict[str, Any], None]:
        with self._get_connection() as connection:
            channel = connection.channel()
            channel.queue_declare(queue=queue, durable=True)
            method_frame, _, body = channel.basic_get(queue)
            if method_frame:
                channel.basic_ack(method_frame.delivery_tag)
                data = body.decode("utf-8")
                return json.loads(data)
            else:
                logger.info("No hay proyectos en la cola")
                exit(0)

    def check_queue(self, name):
        if name not in self.queue_names:
            logger.error(f"Queue {name} no existe")
            raise Exception(f"Queue {name} no existe")
        return name

    def enqueue(self, project: str, client_queue: str):
        queue = self.check_queue(client_queue)
        with self._get_connection() as connection:
            channel = connection.channel()
            channel.queue_declare(queue=queue, durable=True)
            channel.basic_publish(
                exchange="",
                routing_key=queue,
                body=project,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )
            logger.info(f"Project {project} published")
