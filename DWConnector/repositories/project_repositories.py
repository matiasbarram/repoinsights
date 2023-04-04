from ..models.models import Project
from sqlalchemy.orm import Session
from ..models.models import User


class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_projects(self):
        return self.session.query(Project).all()

    def get_main_projects(self):  # non forked
        return self.session.query(Project).filter_by(forked_from=None)

    def get_all_project_with_owner(self):
        return (
            self.session.query(Project, User)
            .join(User)
            .filter(Project.forked_from == None)
            .order_by()
            .all()
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
