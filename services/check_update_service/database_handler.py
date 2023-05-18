from services.check_update_service.connector import DBConnector
from services.check_update_service.models import Project, Commit, Extraction
from sqlalchemy.orm import sessionmaker, aliased
from loguru import logger
from datetime import datetime
from sqlalchemy.sql.schema import Column
from sqlalchemy import func, and_, asc
from sqlalchemy.sql.functions import coalesce

from typing import List, Union, Dict, Any
from .utils import format_dt
from pprint import pprint


class DatabaseHandler:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.Session = sessionmaker(bind=connector.engine)
        self.session = self.Session()

    def get_updated_projects(self) -> List[Dict[str, Any]]:
        enqueue_list = []
        ExtractionAlias = aliased(Extraction)
        CommitAlias = aliased(Commit)

        last_extractions = (
            self.session.query(
                ExtractionAlias.project_id.label("project_id"),
                func.max(ExtractionAlias.date).label("max_extraction_date"),
            )
            .group_by(ExtractionAlias.project_id)
            .subquery()
        )

        last_commits = (
            self.session.query(
                CommitAlias.project_id.label("project_id"),
                func.max(CommitAlias.created_at).label("max_commit_date"),
            )
            .group_by(CommitAlias.project_id)
            .subquery()
        )

        projects_with_dates = (
            self.session.query(
                Project,
                coalesce(
                    last_extractions.c.max_extraction_date,
                    last_commits.c.max_commit_date,
                    datetime.min,
                ).label("last_activity_date"),
            )
            .outerjoin(last_extractions, Project.id == last_extractions.c.project_id)
            .outerjoin(last_commits, Project.id == last_commits.c.project_id)
            .filter(Project.forked_from == None)
            .filter(
                coalesce(
                    last_extractions.c.max_extraction_date,
                    last_commits.c.max_commit_date,
                    datetime.min,
                )
                < datetime.utcnow().date()
            )
            .order_by(asc("last_activity_date"))
            .all()
        )

        for project, last_activity_date in projects_with_dates:
            enqueue_list.append(
                {
                    "enqueue_time": datetime.now(),
                    "attempt": 1,
                    "owner": project.owner.login,
                    "project": project.name,
                    "last_extraction": format_dt(last_activity_date)
                    if last_activity_date != datetime.min
                    else None,
                }
            )
        return enqueue_list
