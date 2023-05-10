from services.check_update_service.connector import DBConnector
from services.check_update_service.models import Project, Commit
from sqlalchemy import func

from typing import List, Union, Dict, Any
from sqlalchemy.orm import sessionmaker
from loguru import logger
from datetime import datetime
from sqlalchemy.sql.schema import Column
from .utils import format_dt


class DatabaseHandler:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.Session = sessionmaker(bind=connector.engine)
        self.session = self.Session()

    def get_last_commit_date(self, project: Project) -> Union[datetime, None]:
        # Query to get the latest commit date for the given project
        last_commit_date = (
            self.session.query(func.max(Commit.created_at).label("last_commit_date"))
            .filter(Commit.project_id == project.id)  # type: ignore
            .scalar()
        )
        if last_commit_date is None:
            logger.warning(
                f"Project {project.owner.login}/{project.name} has no commits"
            )
            return None

        return format_dt(last_commit_date)  # type: ignore

    def get_updated_projects(self) -> List[Dict[str, Any]]:
        enqueue_list = []
        current_date = datetime.now().date()
        projects = (
            self.session.query(Project)
            .filter(
                (Project.last_extraction < current_date)
                | (Project.last_extraction == None)
            )
            .filter(Project.forked_from == None)
            .all()
        )
        for project in projects:
            last_extraction = project.last_extraction
            if project.last_extraction is None:
                last_extraction = self.get_last_commit_date(project)
            else:
                last_extraction = format_dt(last_extraction)  # type: ignore

            enqueue_list.append(
                {
                    "enqueue_time": datetime.now(),
                    "owner": project.owner.login,
                    "project": project.name,
                    "last_extraction": last_extraction,
                }
            )
        return enqueue_list
