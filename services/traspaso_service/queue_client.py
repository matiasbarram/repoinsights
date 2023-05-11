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

    def get_from_queue_curado(
        self, debug: Optional[bool] = None
    ) -> Union[Dict[str, Any], None]:
        if debug:
            return {
                "uuid": "b87d3bc7827341028a110ec3580ae523",
                "owner": "gousiosg",
                "repo": "github-mirror",
                "project_id": 1,
                "since": None,
                "until": "2023-05-09T14:23:16Z",
                "data_types": [
                    "commits",
                    "pull_requests",
                    "issues",
                    "labels",
                    "milestones",
                ],
            }
        self.channel.queue_declare(queue=self.queue_curado)
        method_frame, header_frame, body = self.channel.basic_get(self.queue_curado)
        if method_frame:
            self.channel.basic_ack(method_frame.delivery_tag)
            data = body.decode("utf-8")
            return json.loads(data)
        else:
            return None

    def enqueue(self, project: str):
        self.channel.queue_declare(queue=self.queue_curado)
        self.channel.basic_publish(
            exchange="", routing_key=self.queue_curado, body=project
        )
        logger.info(f"Project {project} published")
