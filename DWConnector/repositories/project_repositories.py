from ..models.models import Project, Commit
from sqlalchemy.orm import Session, sessionmaker, aliased
from sqlalchemy import desc
from ..models.models import User
from ..orm_main import DWConnector


class ProjectRepository:
    def __init__(self):
        self.engine = DWConnector().engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_all_projects(self):
        return self.session.query(Project).where(Project.forked_from == None).all()

    def get_main_projects(self):  # non forked
        return self.session.query(Project).filter_by(forked_from=None).all()

    def get_all_project_with_owner(self):
        return (
            self.session.query(Project, User)
            .join(User)
            .filter(Project.forked_from == None)
            .order_by()
            .all()
        )

    def get_project_with_owner(self, id):
        return (
            self.session.query(Project, User)
            .join(User)
            .filter(Project.id == id)
            .first()
        )

    def get_last_commit(self, id):
        author_alias = aliased(User)
        return (
            self.session.query(Commit, Project, author_alias)
            .select_from(Commit)
            .join(Project, Project.id == Commit.project_id)
            .where(Commit.project_id == id)
            .join(author_alias, author_alias.id == Commit.author_id)
            .order_by(desc(Commit.created_at))
            .first()
        )

    def get_project_by_id(self, id):
        return self.session.query(Project).filter_by(id=id).first()

    def add_project(self, name, description, Project):
        project = Project(name=name, description=description)
        self.session.add(project)
        self.session.commit()

    def update_project(self, id, name, description):
        project = self.get_project_by_id(id)
        if project == None:
            raise Exception("Project not found")
        project.name = name
        project.description = description
        self.session.commit()

    def delete_project(self, id):
        project = self.get_project_by_id(id)
        self.session.delete(project)
        self.session.commit()
