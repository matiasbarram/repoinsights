from check_update_service.connector import DBConnector
from check_update_service.models import Project
from typing import List, Union, Dict, Any
from sqlalchemy.orm import sessionmaker
from loguru import logger
from datetime import datetime


class DatabaseHandler:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.Session = sessionmaker(bind=connector.engine)
        self.session = self.Session()

    def get_updated_projects(self) -> List[Dict[str, Any]]:
        current_date_time = datetime.now()
        projects = (
            self.session.query(Project)
            .filter(
                (Project.last_extraction < current_date_time)
                | (Project.last_extraction == None)
            )
            .filter(Project.forked_from == None)
            .all()
        )
        return [
            {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "owner": project.owner.login,
                "project": project.name,
                "last_extraction": project.last_extraction,
            }
            for project in projects
        ]
