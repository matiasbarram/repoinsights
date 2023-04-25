import os
import json
import random
from typing import Union


class GHToken:
    def get_public_tokens(self, token: Union[str, None]) -> list[str]:
        keys_list = []
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "tokens.json")
        with open(file_path, "r") as keys_file:
            keys_file = json.load(keys_file)
            keys_list = keys_file["keys"]
        return keys_list

    def get_token(self) -> str:
        token_list = self.get_public_tokens(token=None)
        random_token = random.choice(token_list)  # iterate to get a valid token
        return random_token
