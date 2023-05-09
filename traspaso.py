from services.traspaso_service.queue_client import QueueClient
from services.traspaso_service.db_connector.connector import DBConnector
from services.traspaso_service.db_connector.database_handler import DatabaseHandler


from sqlalchemy.orm import sessionmaker, Session
from services.traspaso_service.db_connector.models import Project, User, Commit
from pprint import pprint
from typing import Union
from sqlalchemy import or_
from loguru import logger


class Client:
    def __init__(self, db: DatabaseHandler) -> None:
        self.db = db

    def add_project(self, project_id: int):
        temp_project: Union[Project, None] = self.db.get_or_create(
            Project, self.db.session_temp, create=False, id=project_id
        )
        if temp_project is None:
            raise Exception("Project not exist in temp db")

        consolidated_project: Union[Project, None] = self.db.get_or_create(
            Project, self.db.session_consolidada, create=True, name=temp_project.name
        )

        if consolidated_project is None:
            raise Exception("Project not created in consolidated db")
        return temp_project.id, consolidated_project.id

    def add_commit_users(self, temp_id):
        temp_users = (
            self.db.session_temp.query(User)
            .filter(
                or_(
                    User.id.in_(
                        self.db.session_temp.query(Commit.author_id)
                        .filter(Commit.project_id == temp_id)
                        .distinct()
                    ),
                    User.id.in_(
                        self.db.session_temp.query(Commit.committer_id)
                        .filter(Commit.project_id == temp_id)
                        .distinct()
                    ),
                )
            )
            .all()
        )
        for user in temp_users:
            conslidada_user = self.db.get_or_create(
                model=User,
                session=self.db.session_consolidada,
                login=user.login,
                create=False,
            )
            if conslidada_user is None:
                self.db.get_or_create(
                    model=User,
                    session=self.db.session_consolidada,
                    login=user.login,
                    name=user.name,
                    company=user.company,
                    location=user.location,
                    email=user.email,
                    created_at=user.created_at,
                    type=user.type,
                )

    def add_commits(self, temp_project_id, consolidated_project_id):
        logger.warning(f"Project: {consolidated_project_id}")
        author_id = None
        committer_id = None
        temp_commits = (
            self.db.session_temp.query(Commit)
            .filter(Commit.project_id == temp_project_id)
            .all()
        )
        for commit in temp_commits:
            logger.warning(f"Commit: {commit.sha}")
            consolidated_commit = self.db.get_or_create(
                model=Commit,
                session=self.db.session_consolidada,
                project_id=consolidated_project_id,
                sha=commit.sha,
                create=False,
            )

            logger.warning(f"Author: {commit.author_id}")
            if consolidated_commit is None:
                if commit.author_id is not None:
                    author_id = self.db.get_or_create(
                        model=User,
                        session=self.db.session_consolidada,
                        id=commit.author_id,
                        create=False,
                    ).id
                if commit.committer_id is not None:
                    committer_id = self.db.get_or_create(
                        model=User,
                        session=self.db.session_consolidada,
                        id=commit.committer_id,
                        create=False,
                    ).id

                consolidated_commit = self.db.get_or_create(
                    model=Commit,
                    session=self.db.session_consolidada,
                    sha=commit.sha,
                    author_id=author_id,
                    committer_id=committer_id,
                    project_id=consolidated_project_id,
                    created_at=commit.created_at,
                    # message=commit.message,
                )


def main():
    queue_client = QueueClient()
    project = queue_client.get_from_queue_curado(debug=True)
    if project is None:
        return

    print(project)
    db = DBConnector()
    db_handler = DatabaseHandler(db)
    client = Client(db_handler)
    temp_project_id, cosolidada_project_id = client.add_project(project["project_id"])
    # client.add_forks(temp_project_id, cosolidada_project_id)
    client.add_commit_users(temp_project_id)
    client.add_commits(temp_project_id, cosolidada_project_id)


if __name__ == "__main__":
    main()
