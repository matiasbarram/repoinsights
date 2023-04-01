import sqlalchemy as db
import os
from dotenv import load_dotenv

load_dotenv()


class DW_extract:
    def __init__(self) -> None:
        self.user = os.environ["MYSQL_USER"]
        self.password = os.environ["MYSQL_PASSWORD"]
        self.database = os.environ["MYSQL_DB"]

    def connect(self):
        engine = db.create_engine(
            f"mysql+pymysql://{self.user}:{self.password}@/db?host=localhost?port=3306"
        )
