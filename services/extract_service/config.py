import os
import json
import random
from typing import Union, List, Dict, Tuple
import requests
from datetime import datetime
from loguru import logger


class GHToken:
    def get_public_tokens(self, many: bool = False) -> List[str]:
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
            tokens_with_calls.append((token, calls_left))

        # Sort tokens by remaining calls, in descending order
        tokens_with_calls.sort(key=lambda x: x[1], reverse=True)

        if many:
            return tokens_with_calls

        return [token for token, calls_left in tokens_with_calls]

    def get_token_lowest_wait_time(self) -> Tuple:
        tokens = self.get_public_tokens()
        wait_times = []
        for token in tokens:
            headers = {"Authorization": f"token {token}"}
            response = requests.get(
                "https://api.github.com/rate_limit", headers=headers
            )
            wait_times.append(
                {
                    "token": token,
                    "time": int(response.json()["resources"]["core"]["reset"]),
                }
            )
        wait_times.sort(key=lambda x: x["time"])
        logger.debug(wait_times)
        return wait_times[0]["token"], wait_times[0]["time"]

    def get_token(self) -> str:
        token_list = self.get_public_tokens()
        random_token = random.choice(token_list)  # iterate to get a valid token
        return random_token
