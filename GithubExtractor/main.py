from typing import Union
from github import Github
import json
import random


class GHRequest:
    def __init__(self, token=None) -> None:
        self.token = self.get_token(token=token)
        if not self.test_token():
            raise Exception("Error de token. Test")

    def get_token(self, token: Union[str, None]) -> str:
        keys_list = []
        with open("GH_KEYS.json", "r") as keys_file:
            keys_file = json.load(keys_file)
            keys_list: list = keys_file["keys"]

        random_key: str = random.choice(keys_list)
        return random_key

    def test_token(self) -> bool:
        github_api = Github(self.token)
        try:
            me: str = github_api.get_user().login
            print(f"Hello! {me}")
            return True
        except Exception as e:
            return False

    def get_github_data():
        pass


gh_request = GHRequest()
