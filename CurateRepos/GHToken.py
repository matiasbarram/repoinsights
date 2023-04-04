import random
from typing import Union
from github import Github
import json
import os


class GHToken:
    def test_token(self, token: str):
        github_api = Github(token)
        try:
            me: str = github_api.get_user().login
            print(f"Hello! {me}")
            return github_api
        except Exception as e:
            tokens = self.get_public_tokens(token=None)
            random_token = random.choice(tokens)
            print(f"Token {token} is not valid. Trying {random_token}")
            self.test_token(random_token)

    def get_public_tokens(self, token: Union[str, None]) -> list[str]:
        keys_list = []
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "GH_KEYS.json")
        with open(file_path, "r") as keys_file:
            keys_file = json.load(keys_file)
            keys_list = keys_file["keys"]
        return keys_list

    def get_github_connector(self, token_list: list):
        token: str = random.choice(token_list)
        github_connector = self.test_token(token=token)
        while not github_connector:
            token: str = random.choice(token_list)
            github_connector = self.test_token(token=token)

        return github_connector

    def get_token(self) -> str:
        token_list = self.get_public_tokens(token=None)
        random_token = random.choice(token_list)  # iterate to get a valid token
        return random_token
