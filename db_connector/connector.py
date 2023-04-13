from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


class DBConnector:
    def __init__(self, db) -> None:
        self.CONSOLIDADA_USER = os.getenv("CONSOLIDADA_USER")
        self.CONSOLIDADA_PASSWORD = os.getenv("CONSOLIDADA_PASSWORD")
        self.CONSOLIDADA_DATABASE = os.getenv("CONSOLIDADA_DB")
        self.CONSOLIDADA_IP = os.getenv("CONSOLIDADA_IP")
        self.CONSOLIDADA_PORT = os.getenv("CONSOLIDADA_PORT")
        self.TEMP_USER = os.getenv("TEMP_USER")
        self.TEMP_PASSWORD = os.getenv("TEMP_PASSWORD")
        self.TEMP_DATABASE = os.getenv("TEMP_DB")
        self.TEMP_IP = os.getenv("TEMP_IP")
        self.TEMP_PORT = os.getenv("TEMP_PORT")
        print(
            {
                "CONSOLIDADA_USER": self.CONSOLIDADA_USER,
                "CONSOLIDADA_PASSWORD": self.CONSOLIDADA_PASSWORD,
                "CONSOLIDADA_DATABASE": self.CONSOLIDADA_DATABASE,
                "CONSOLIDADA_IP": self.CONSOLIDADA_IP,
                "CONSOLIDADA_PORT": self.CONSOLIDADA_PORT,
                "TEMP_USER": self.TEMP_USER,
                "TEMP_PASSWORD": self.TEMP_PASSWORD,
                "TEMP_DATABASE": self.TEMP_DATABASE,
                "TEMP_IP": self.TEMP_IP,
                "TEMP_PORT": self.TEMP_PORT,
            }
        )
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
            f"postgresql+psycopg2://{self.CONSOLIDADA_USER}:{self.CONSOLIDADA_PASSWORD}@{self.CONSOLIDADA_IP}:{self.CONSOLIDADA_PORT}/{self.CONSOLIDADA_DATABASE}"
        )
        return engine

    def __init_temp(self):
        engine = create_engine(
            f"postgresql+psycopg2://{self.TEMP_USER}:{self.TEMP_PASSWORD}@{self.TEMP_IP}:{self.TEMP_PORT}/{self.TEMP_DATABASE}"
        )
        return engine

    def test_connection(self) -> None:
        try:
            conn = self.engine.connect()
            print("Conexión exitosa!")
        except Exception as e:
            print("Error de conexión: ", str(e))


def main():
    env = "local"
    if env == "local":
        load_dotenv(".env.local")
    elif env == "prd":
        load_dotenv(".env.prd")

    db_consolidada = DBConnector(db="consolidada")
    db_temp = DBConnector(db="temp")


if __name__ == "__main__":
    main()
