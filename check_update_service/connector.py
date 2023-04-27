from sqlalchemy import create_engine, select, Select, Engine, URL
import os

CONSOLIDADA_USER = os.getenv("CONSOLIDADA_USER")
CONSOLIDADA_PASSWORD = os.getenv("CONSOLIDADA_PASS")
CONSOLIDADA_DATABASE = os.getenv("CONSOLIDADA_DB")
CONSOLIDADA_IP = os.getenv("CONSOLIDADA_IP")
CONSOLIDADA_PORT = os.getenv("CONSOLIDADA_PORT")


class DBConnector:
    def __init__(
        self,
    ) -> None:
        self.engine = self.__init_consolidada()

    def __init_consolidada(self):
        engine = create_engine(
            f"postgresql+psycopg2://{CONSOLIDADA_USER}:{CONSOLIDADA_PASSWORD}@{CONSOLIDADA_IP}:{CONSOLIDADA_PORT}/{CONSOLIDADA_DATABASE}"
        )
        self.test_connection(engine)
        return engine

    def test_connection(self, engine: Engine) -> None:
        try:
            engine.connect()
            print("Conexión exitosa!")
        except Exception as e:
            print("Error de conexión: ", str(e))
