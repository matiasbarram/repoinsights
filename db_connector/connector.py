from sqlalchemy import create_engine, select, Select
import os

CONSOLIDADA_USER = os.getenv("CONSOLIDADA_USER")
CONSOLIDADA_PASSWORD = os.getenv("CONSOLIDADA_PASSWORD")
CONSOLIDADA_DATABASE = os.getenv("CONSOLIDADA_DB")
CONSOLIDADA_IP = os.getenv("CONSOLIDADA_IP")
CONSOLIDADA_PORT = os.getenv("CONSOLIDADA_PORT")

TEMP_USER = os.getenv("TEMP_USER")
TEMP_PASSWORD = os.getenv("TEMP_PASSWORD")
TEMP_DATABASE = os.getenv("TEMP_DB")
TEMP_IP = os.getenv("TEMP_IP")
TEMP_PORT = os.getenv("TEMP_PORT")


class DBConnector:
    def __init__(self, db) -> None:
        if db == "consolidada":
            self.engine = self.__init_consolidada()
        elif db == "temp":
            self.engine = self.__init_temp()
        else:
            raise Exception("No se reconoce la base de datos")

        self.test_connection()
        self.conn = self.engine.connect()

    def __init_consolidada(self):
        engine = create_engine(
            f"postgresql+psycopg2://{CONSOLIDADA_USER}:{CONSOLIDADA_PASSWORD}@{CONSOLIDADA_IP}:{CONSOLIDADA_PORT}/{CONSOLIDADA_DATABASE}"
        )
        return engine

    def __init_temp(self):
        engine = create_engine(
            f"postgresql+psycopg2://{TEMP_USER}:{TEMP_PASSWORD}@{TEMP_IP}:{TEMP_PORT}/{TEMP_DATABASE}"
        )
        return engine

    def test_connection(self) -> None:
        try:
            conn = self.engine.connect()
            print("Conexión exitosa!")
        except Exception as e:
            print("Error de conexión: ", str(e))
