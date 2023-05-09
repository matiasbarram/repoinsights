import pika
import os
from loguru import logger
import json
from typing import Dict, Any, Union, Optional

"""
{
    "owner": "mavam", 
    "repo": "stat-cookbook", 
    "since": "May 18, 2013, 12:00 AM", 
    "until": "June 17, 2013, 12:00 AM", 
    "data_types": ["commits", "pull_requests", "issues", "labels", "milestones"]
}
"""


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
                "owner": "mavam",
                "repo": "stat-cookbook",
                "project_id": 41,
                "since": "2013-01-31T03:46:46Z",
                "until": "2023-05-08T21:41:05Z",
                "data_types": [
                    "commits",
                    "pull_requests",
                    "issues",
                    "labels",
                    "milestones",
                ],
            }

        self.channel.queue_declare(queue=self.queue_curado)
        method_frame, header_frame, body = self.channel.basic_get(self.queue_pendientes)
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
