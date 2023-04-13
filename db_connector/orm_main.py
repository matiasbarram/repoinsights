from sqlalchemy import create_engine, select, Select
import os


class DBConnector:
    def __init__(self, user, ip, password, port, database) -> None:
        self.engine = self.__create_connector(user, ip, password, port, database)
        self.test_connection()
        self.conn = self.engine.connect()

    def __create_connector(self, user, ip, password, port, database):
        engine = create_engine(
            f"postgresql+psycopg2://{user}:{password}@{ip}:{port}/{database}"
        )
        return engine

    def test_connection(self) -> None:
        try:
            conn = self.engine.connect()
            print("Conexión exitosa!")
        except Exception as e:
            print("Error de conexión: ", str(e))
