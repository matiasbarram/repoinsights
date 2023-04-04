from github import Github
import os
import json
import random
from typing import Union


class GHToken:
    def test_token(self, token) -> Union[Github, bool]:
        github_api = Github(token)
        try:
            me: str = github_api.get_user().login
            print(f"Hello! {me}")
            return github_api
        except Exception as e:
            return False

    def get_public_tokens(self, token: Union[str, None]) -> list:
        keys_list = []
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "GH_KEYS.json")
        with open(file_path, "r") as keys_file:
            keys_file = json.load(keys_file)
            keys_list: list = keys_file["keys"]
        return keys_list

    def get_github_connector(self, token_list: list) -> str:
        token: str = random.choice(token_list)
        github_connector = self.test_token(token=token)
        while not github_connector:
            token: str = random.choice(token_list)
            github_connector = self.test_token(token=token)

        return github_connector
