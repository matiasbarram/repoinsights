from sqlalchemy.orm import sessionmaker
from .models import User, Project  # Importe las clases adicionales según sea necesario
from .connector import DBConnector
from sqlalchemy import Engine
from .connector import DBConnector
from pprint import pprint
from .user_handler import UserHandler


class DatabaseHandler:
    def __init__(self, connector: DBConnector):
        self.Session_consolidada = sessionmaker(bind=connector.consolidada_engine)
        self.session_consolidada = self.Session_consolidada()

        self.Session_temp = sessionmaker(bind=connector.temp_engine)
        self.session_temp = self.Session_temp()

        self.user_handler = UserHandler(self.session_temp, self.session_consolidada)

    def create_project(self, **kwargs):
        new_project = Project(**kwargs)
        self.session_temp.add(new_project)
        self.session_temp.commit()
        return {"created": True, "project": new_project}

    # Agregue métodos adicionales para otras operaciones de base de datos aquí

    def close(self):
        self.session_temp.close()
