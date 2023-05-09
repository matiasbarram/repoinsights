from .connector import DBConnector
from .models import (
    User,
    Project,
    Commit,
    CommitParent,
    Issue,
    IssueComment,
    PullRequest,
    PullRequestComment,
    Watcher,
    ProjectMember,
)
from pprint import pprint
from typing import List, Union, Dict, Any
from sqlalchemy.orm import sessionmaker, Session
from typing import Union, List, Optional
from loguru import logger


class DatabaseHandler:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.Session_consolidada = sessionmaker(bind=connector.consolidada_engine)
        self.session_consolidada = self.Session_consolidada()

        self.Session_temp = sessionmaker(bind=connector.temp_engine)
        self.session_temp = self.Session_temp()

    def get_or_create(
        self,
        model: Union[
            User,
            Project,
            Commit,
            CommitParent,
            Issue,
            IssueComment,
            PullRequest,
            PullRequestComment,
            Watcher,
        ],
        session: Session,
        create: Optional[bool] = True,
        **kwargs,
    ):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            logger.debug("Instance already exists")
            return instance
        elif create:
            try:
                logger.debug("Creating new instance")
                instance = model(**kwargs)
                session.add(instance)
                session.commit()
                return instance
            except Exception as e:
                logger.error(f"Error creating")
                raise BaseException(e)
        else:
            logger.debug("Instance does not exist and not created")
            return None
