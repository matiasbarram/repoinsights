from db_connector.connector import DBConnector
from db_connector.database_handler import DatabaseHandler
import json
from github_service.github_api.user import GHUser
from pprint import pprint


class LoadData:
    def __init__(self):
        self.temp_db = DatabaseHandler(DBConnector())

    def load_temp_db(self, results):
        for result in results:
            if result["name"] == "owner":
                gh_user: GHUser = result["data"]
                create_response = self.temp_db.create_user(gh_user.to_dict())
                if create_response["created"]:
                    print("User created successfully")
                else:
                    print("User already exists")
                    pprint(create_response["user"])
        # self.db.insert_commits(results[0])
