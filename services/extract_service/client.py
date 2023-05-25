import json
from typing import Dict, Any, List, Union
from datetime import datetime
from loguru import logger
import uuid

from .utils.utils import format_dt, api_date
from services.extract_service.extract_module.extract_client import ExtractDataClient
from .queue_module.enqueue_client import QueueClient
from .load_module.load_client import LoadDataClient
from .excepctions.exceptions import LoadError


class InsightsClient:
    def __init__(self, data_types: List) -> None:
        self.data_types = data_types
        self.until = datetime.now()
        self.uuid = uuid.uuid4().hex
        self.project_id = None
        self.queue_client = QueueClient()

        (
            self.pending_repo,
            self.owner,
            self.repo,
            self.since,
        ) = self.get_from_pendientes()

        self.extract_data = ExtractDataClient(
            owner=self.owner,
            repo=self.repo,
            since=self.since,
            until=self.until,
            data_types=self.data_types,
        )

    def get_from_pendientes(self):
        pending_project = self.queue_client.get_from_queue()
        if pending_project:
            pending_repo = pending_project
            owner = pending_repo["owner"]
            repo = pending_repo["project"]
            since: Union[datetime, None] = (
                api_date(pending_repo["last_extraction"])
                if pending_repo["last_extraction"]
                else None
            )
            logger.critical("QUEUE pendientes {project}", project=pending_repo)
            return pending_repo, owner, repo, since
        else:
            logger.critical("No hay proyectos pendientes")
            exit(0)

    def enqueue_to_modificacion(self, type, **kwargs):
        project_data = {}
        if type == "rename":
            project_data = {
                "action": "delete",
                "project": {"owner": self.owner, "repo": self.repo},
            }
        elif type == "delete":
            if "new" not in kwargs:
                raise LoadError("No se especificó el nuevo nombre del proyecto")
            new = kwargs["new"]
            project_data = {
                "action": "delete",
                "current": {"owner": self.owner, "repo": self.repo},
                "new": {"owner": new["owner"], "repo": new["repo"]},
            }

        json_data = json.dumps(project_data)
        self.queue_client.enqueue(json_data, "modificacion")

    def enqueue_to_pendientes(self):
        if self.pending_repo is None:
            raise LoadError("No hay proyecto pendiente")

        self.pending_repo["enqueue_time"] = datetime.now().isoformat()
        self.pending_repo["attempt"] = self.pending_repo["attempt"] + 1
        json_data = json.dumps(self.pending_repo)
        self.queue_client.enqueue(json_data, "pendientes")

    def extract(self) -> List[Dict[str, Any]]:
        logger.critical(
            "Extracting from GitHub {owner}/{project} DESDE -> {since} HASTA -> {until} {data_types}",
            owner=self.owner,
            project=self.repo,
            since=self.since,
            until=self.until,
            data_types=self.data_types,
        )
        data = self.extract_data.extract()
        return data

    def load(self, results) -> None:
        logger.critical("Loading to TEMP DB")
        try:
            load_client = LoadDataClient(results, self.uuid, self.owner, self.repo)
            load_client.load_to_temp_db()
            self.project_id = load_client.get_project_id()
        except Exception as e:
            logger.critical(f"Error loading data to TEMP DB: {e}")
            raise LoadError("Error loading data to TEMP DB", e)

    def enqueue_to_curado(self) -> None:
        project_data = {
            "uuid": self.uuid,
            "owner": self.owner,
            "repo": self.repo,
            "project_id": self.project_id,
            "since": format_dt(self.since) if self.since else None,
            "until": format_dt(self.until) if self.until else None,
            "data_types": self.data_types,
        }
        json_data = json.dumps(project_data)
        self.queue_client.enqueue(json_data, "curado")
        logger.critical("Project ENQUEUE to CURADO published")
