from sqlalchemy.orm import sessionmaker
from .models import User, Project  # Importe las clases adicionales según sea necesario
from .connector import DBConnector
from sqlalchemy import Engine


class DatabaseHandler:
    def __init__(self, db_engine: Engine):
        self.Session = sessionmaker(bind=db_engine)
        self.session = self.Session()

    def create_user(self, user_data: dict):
        existing_user = (
            self.session.query(User).filter_by(login=user_data["login"]).first()
        )
        if existing_user:
            for key, value in user_data.items():
                setattr(existing_user, key, value)
            self.session.commit()
            return {"created": False, "user": existing_user}
        else:
            new_user = User(**user_data)
            self.session.add(new_user)
            self.session.commit()
            return {"created": True, "user": new_user}

    def create_project(self, **kwargs):
        new_project = Project(**kwargs)
        self.session.add(new_project)
        self.session.commit()
        return {"created": True, "project": new_project}

    # Agregue métodos adicionales para otras operaciones de base de datos aquí

    def close(self):
        self.session.close()
