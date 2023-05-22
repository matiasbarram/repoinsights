import requests
from loguru import logger
from typing import Optional, Dict, Union
import json
import redis
import time
import os
from datetime import datetime

from services.extract_service.utils.utils import api_date, format_dt
from services.extract_service.config import GHToken
from services.extract_service.excepctions.exceptions import (
    RateLimitExceededError,
    NoMoreTokensError,
    ProjectNotFoundError,
)


class GitHubAPI:
    def __init__(self):
        self.cache = Cache()
        self.tokens_handler = GHToken()
        tokens = self.tokens_handler.get_public_tokens()
        self.token = tokens[0]
        self.headers = {"Authorization": f"token {self.token}"}

    def rate_limit_handling(self, func, *args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except RateLimitExceededError:
                try:
                    self._handle_no_more_calls()
                    self.rate_limit_handling(func, *args, **kwargs)
                except NoMoreTokensError:
                    logger.critical("No more tokens")
                    self._handle_wait_time()
                    self.rate_limit_handling(func, *args, **kwargs)

    def update_token(self, new_token: str):
        self.token = new_token
        self.headers["Authorization"] = f"token {self.token}"

    def _handle_no_more_calls(self):
        tokens = self.tokens_handler.get_public_tokens(only_token=False)
        for token, calls, reset_time in tokens:
            if calls > 200:
                logger.warning(f"Token changed {token[-10:]}")
                self.update_token(token)
                return
        logger.warning("No more tokens available")
        raise NoMoreTokensError("No more tokens available")

    def _handle_wait_time(self):
        tokens = self.tokens_handler.get_public_tokens(only_token=False)
        tokens.sort(key=lambda x: x[2])
        wait_time = tokens[0][2] - time.time()
        logger.warning(f"Waiting {wait_time} seconds")
        time.sleep(wait_time)
        self.update_token(tokens[0][0])

    def get(
        self,
        url,
        params=None,
        name: Optional[str] = None,
        headers: Optional[Dict] = None,
    ):
        try:
            if headers is not None:
                self.headers.update(headers)
            response = requests.get(url, headers=self.headers, params=params)
            logger.debug(
                "{name} \t {current}/{limit}",
                current=response.headers["X-RateLimit-Remaining"],
                limit=response.headers["X-RateLimit-Limit"],
                name=name,
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
            elif e.response.status_code == 451:
                logger.error("Proyecto eliminado")
                ProjectNotFoundError("Proyecto eliminado")
            elif e.response.status_code == 404:
                logger.error("Proyecto no encontrado")
                ProjectNotFoundError("Proyecto no encontrado")
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
        if params.get("since") is not None:
            logger.warning(
                "{name} \t Since: {type} - {since}",
                type=type(params["since"]),
                since=params["since"],
                name=name,
            )
            since = params["since"]
            if type(since) == "datetime":
                params["since"] = format_dt(since)
        if params.get("until") is not None:
            until: datetime = params["until"]
            if type(until) == datetime:
                params["until"] = format_dt(until)

        while url:
            response = self.get(url, params=params, headers=headers, name=name)
            if response is None:
                break

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
            created_at = api_date(elemento["created_at"])
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
        self.redis_cache = redis.StrictRedis(
            host=self.redis_host, port=self.redis_port, db=self.redis_db
        )

    def get(self, key):
        value = self.redis_cache.get(key)
        return json.loads(value.decode("utf-8")) if value else None

    def set(self, key, value, expiry=None):
        serialized_value = json.dumps(value)
        self.redis_cache.set(key, serialized_value, ex=expiry)

    def has(self, key):
        return self.redis_cache.exists(key)
