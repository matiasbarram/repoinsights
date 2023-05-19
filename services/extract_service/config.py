import os
import json
import random
from typing import Union, List, Dict, Tuple
import requests
from datetime import datetime
from loguru import logger


class GHToken:
    def get_public_tokens(self, only_token: bool = True):
        keys_list = []
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "tokens.json")
        with open(file_path, "r") as keys_file:
            keys_file = json.load(keys_file)
            keys_list = keys_file["keys"]

        tokens_with_calls = []
        for token in keys_list:
            headers = {"Authorization": f"token {token}"}
            response = requests.get(
                "https://api.github.com/rate_limit", headers=headers
            )
            calls_left = int(response.json()["resources"]["core"]["remaining"])
            reset_time = int(response.json()["resources"]["core"]["reset"])
            tokens_with_calls.append((token, calls_left, reset_time))

        # Sort tokens by remaining calls, in descending order
        tokens_with_calls.sort(key=lambda x: x[1], reverse=True)
        if only_token:
            return [token for token, _, _ in tokens_with_calls]
        return tokens_with_calls

    def get_token_lowest_wait_time(self) -> Tuple:
        tokens = self.get_public_tokens()
        tokens.sort(key=lambda x: x[2])
        return tokens[0]
