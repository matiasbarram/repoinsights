from .extract_client import ExtractDataClient
from .load_client import LoadDataClient
from .enqueue_client import QueueClient
import json
from typing import Dict, Any, List
from datetime import datetime
from ..utils.utils import format_dt, gh_api_to_datetime
from loguru import logger


class EmptyQueueError(Exception):
    pass


class ExtractError(Exception):
    pass


class LoadError(Exception):
    pass


class InsightsClient:
    def __init__(self, data_types: List) -> None:
        self.data_types = data_types
        self.until = datetime.now()

    def get_from_pendientes(self):
        repo = QueueClient().get_from_queue()
        if repo:
            self.owner = repo["owner"]
            self.repo = repo["project"]
            self.since: datetime = gh_api_to_datetime(repo["last_extraction"])

            logger.critical("QUEUE pendientes {project}", project=repo)
        else:
            raise EmptyQueueError("No hay proyectos en la cola")

    def extract(self) -> List[Dict[str, Any]]:
        logger.critical(f"Extracting data from GitHub")
        extract_data = ExtractDataClient(
            owner=self.owner,
            repo=self.repo,
            since=self.since,
            until=self.until,
            data_types=self.data_types,
        )
        try:
            data = extract_data.extract()
            return data
        except Exception as e:
            logger.critical(f"Error extracting data from GitHub: {e}")
            raise ExtractError("Error extracting data from GitHub")

    def load(self, results) -> None:
        logger.critical(f"Loading to TEMP DB")
        try:
            load_client = LoadDataClient(results)
            load_client.load_to_temp_db()
            self.project_id = load_client.get_project_id()
        except Exception as e:
            logger.critical(f"Error loading data to TEMP DB: {e}")
            raise LoadError("Error loading data to TEMP DB")

    def enqueue_to_curado(self) -> None:
        project_data = {
            "owner": self.owner,
            "repo": self.repo,
            "project_id": self.project_id,
            "since": format_dt(self.since) if self.since else None,
            "until": format_dt(self.until) if self.until else None,
            "data_types": self.data_types,
        }
        json_data = json.dumps(project_data)
        QueueClient().enqueue(json_data)
        logger.critical(f"Project ENQUEUE to CURADO published")
