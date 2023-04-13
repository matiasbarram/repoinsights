from sqlalchemy.orm import sessionmaker
from .models import User, Project  # Importe las clases adicionales según sea necesario
from .connector import DBConnector
from sqlalchemy import Engine
from .connector import DBConnector
from pprint import pprint


class DatabaseHandler:
    def __init__(self, connector: DBConnector):
        self.Session_consolidada = sessionmaker(bind=connector.consolidada_engine)
        self.session_consolidada = self.Session_consolidada()

        self.Session_temp = sessionmaker(bind=connector.temp_engine)
        self.session_temp = self.Session_temp()

    def create_user(self, user_data: dict):
        user_consolidada = (
            self.session_consolidada.query(User)
            .filter_by(login=user_data["login"])
            .first()
        )
        if user_consolidada:
            return {
                "created": False,
                "user": {
                    column.name: getattr(user_consolidada, column.name)
                    for column in User.__table__.columns
                },
            }
        print("No existe en consolidada")
        existing_user = (
            self.session_temp.query(User).filter_by(login=user_data["login"]).first()
        )
        if existing_user:
            for key, value in user_data.items():
                setattr(existing_user, key, value)
            self.session_temp.commit()
            return {"created": False, "user": existing_user}
        else:
            new_user = User(**user_data)
            self.session_temp.add(new_user)
            self.session_temp.commit()
            return {"created": True, "user": new_user}

    def create_project(self, **kwargs):
        new_project = Project(**kwargs)
        self.session_temp.add(new_project)
        self.session_temp.commit()
        return {"created": True, "project": new_project}

    # Agregue métodos adicionales para otras operaciones de base de datos aquí

    def close(self):
        self.session_temp.close()
