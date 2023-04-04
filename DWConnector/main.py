from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.models import Project, User
from .repositories.project_repositories import ProjectRepository


import os
import json

USER = os.environ["GHTORRENT_USER"]
PASSWORD = os.environ["GHTORRENT_PASSWORD"]
DATABASE = os.environ["GHTORRENT_DB"]
IP = os.environ["GHTORRENT_IP"]
PORT = os.environ["GHTORRENT_PORT"]


class DWConnector:
    def __init__(self) -> None:
        self.engine = self.__create_connector()
        self.test_connection()

    def __create_connector(self):
        engine = create_engine(
            f"mysql+mysqlconnector://{USER}:{PASSWORD}@{IP}:{PORT}/{DATABASE}"
        )
        return engine

    def test_connection(self) -> None:
        try:
            conn = self.engine.connect()
            print("Conexión exitosa!")
        except Exception as e:
            print("Error de conexión: ", str(e))

    def get_repos(self) -> list:
        repos_data = []
        Session = sessionmaker(bind=self.engine)
        session = Session()
        repositories = ProjectRepository(session)
        projects = repositories.get_all_project_with_owner()
        project: Project
        user: User
        for project, user in projects:
            repo_data = {"id": project.id, "name": f"{user.login}/{project.name}"}
            repos_data.append(repo_data)

        print(json.dumps(repos_data))
        return repos_data
