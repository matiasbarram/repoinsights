from sqlalchemy import create_engine, select, Select
from sqlalchemy.orm import sessionmaker
from .models.models import Project, User
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
        self.conn = self.engine.connect()

    def __create_connector(self):
        engine = create_engine(
            f"postgresql+psycopg2://{USER}:{PASSWORD}@{IP}:{PORT}/{DATABASE}"
        )
        return engine

    def test_connection(self) -> None:
        try:
            conn = self.engine.connect()
            print("Conexión exitosa!")
        except Exception as e:
            print("Error de conexión: ", str(e))
