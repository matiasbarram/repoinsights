import psycopg2
import os

user = os.environ["CONSOLIDADA_USER"]
host = os.environ["CONSOLIDADA_IP"]
port = os.environ["CONSOLIDADA_PORT"]
database = os.environ["CONSOLIDADA_DB"]
password = os.environ["CONSOLIDADA_PASS"]


class ConsolidadaConnection:
    def __init__(self):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def get_connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
        )
