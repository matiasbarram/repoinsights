from sqlalchemy import create_engine, select, Select, Engine
import os

TEMP_USER = os.getenv("TEMP_USER")
TEMP_PASSWORD = os.getenv("TEMP_PASS")
TEMP_DATABASE = os.getenv("TEMP_DB")
TEMP_IP = os.getenv("TEMP_IP")
TEMP_PORT = os.getenv("TEMP_PORT")


class DBConnector:
    def __init__(self):
        self.engine = self.__init_temp()
        self.test_connection(self.engine)

    def __init_temp(self):
        engine = create_engine(
            f"postgresql+psycopg2://{TEMP_USER}:{TEMP_PASSWORD}@{TEMP_IP}:{TEMP_PORT}/{TEMP_DATABASE}"
        )
        return engine

    def test_connection(self, engine: Engine) -> None:
        try:
            engine.connect()
            print("Conexión exitosa!")
        except Exception as e:
            print("Error de conexión: ", str(e))
