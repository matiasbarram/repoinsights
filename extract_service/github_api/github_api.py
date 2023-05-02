import requests
from loguru import logger
from ..utils.utils import gh_api_to_datetime
from ..config import GHToken
from typing import Optional, Dict, Any, List, Set, Iterator, Union
import json
import redis
import time
import os


class RateLimitExceededError(Exception):
    pass


class GitHubAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": f"token {self.token}"}

    def update_token(self, new_token):
        self.token = new_token
        self.headers["Authorization"] = f"token {self.token}"

    def get(self, url, params=None, headers: Optional[Dict] = None):
        try:
            if headers is not None:
                self.headers.update(headers)
            response = requests.get(url, headers=self.headers, params=params)
            logger.debug(
                "{current}/{limit}",
                current=response.headers["X-RateLimit-Remaining"],
                limit=response.headers["X-RateLimit-Limit"],
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            if (
                e.response.status_code == 403
                and "X-RateLimit-Remaining" in e.response.headers
                and int(e.response.headers["X-RateLimit-Remaining"]) == 0
            ):
                raise RateLimitExceededError("GitHub API rate limit exceeded.")
            else:
                raise e

    def _realizar_solicitud_paginada(
        self,
        name: str,
        url: Union[str, None],
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ):
        if params is None:
            params = {}
        params.setdefault("per_page", 100)
        elementos = []
        pag = 1
        while url:
            response = self.get(url, params=params, headers=headers)
            elementos.extend(response.json())
            logger.info(f"{name} Pagina {pag}: {len(response.json())} elementos")
            pag += 1
            if "next" in response.links:
                url = response.links["next"]["url"]
            else:
                url = None
        return elementos

    def _filtrar_por_fecha(self, elementos, since=None, until=None):
        if since is None and until is None:
            return elementos
        resultados = []
        for elemento in elementos:
            created_at = gh_api_to_datetime(elemento["created_at"])
            if since and created_at < since:
                continue
            if until and created_at > until:
                continue
            resultados.append(elemento)

        return resultados


class Cache:
    def __init__(self):
        self.redis_host = os.environ["REDIS_HOST"]
        self.redis_port: int = int(os.environ["REDIS_PORT"])
        self.redis_db = int(os.environ["REDIS_DB"])
        self.cache = redis.StrictRedis(
            host=self.redis_host, port=self.redis_port, db=self.redis_db
        )

    def get(self, key):
        value = self.cache.get(key)
        return json.loads(value.decode("utf-8")) if value else None

    def set(self, key, value, expiry=None):
        serialized_value = json.dumps(value)
        self.cache.set(key, serialized_value, ex=expiry)

    def has(self, key):
        return self.cache.exists(key)


class GitHubResource:
    def __init__(self, api: GitHubAPI):
        self.api = api
        self.cache = Cache()

    def _handle_rate_limit_exceeded(self, tokens_iter):
        try:
            new_token = next(tokens_iter)
            print("New token: ", new_token)
            self.api.update_token(new_token)
        except StopIteration:
            token, wait_time = GHToken().get_token_lowest_wait_time()
            logger.warning(
                "No more tokens! Waiting for {wait_time} seconds", wait_time=wait_time
            )
            time.sleep(wait_time - time.time() + 10)
            self.api.update_token(token)

    def invoke_with_rate_limit_handling(self, func, tokens_iter, *args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except RateLimitExceededError:
                self._handle_rate_limit_exceeded(tokens_iter)
