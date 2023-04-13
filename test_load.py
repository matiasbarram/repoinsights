from db_connector.connector import DBConnector
from db_connector.database_handler import DatabaseHandler
import json
from github_service.github_api.user import GHUser


class LoadData:
    def __init__(self, db: str):
        self.engine = DBConnector(db).engine
        self.db = DatabaseHandler(self.engine)

    def load_temp_db(self, results):
        for result in results:
            if result["name"] == "owner":
                gh_user: GHUser = result["data"]
                create_response = self.db.create_user(gh_user.to_dict())
                if create_response["created"]:
                    print("User created successfully")
                else:
                    print("User already exists")
        # self.db.insert_commits(results[0])
