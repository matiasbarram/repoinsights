from pprint import pprint
import requests
from loguru import logger
from typing import Any, Optional, Dict, Union
import json
import redis
import time
import os
from datetime import datetime, timedelta

from services.extract_service.utils.utils import api_date, format_dt
from services.extract_service.config import GHToken
from services.extract_service.excepctions.exceptions import (
    RateLimitExceededError,
    NoMoreTokensError,
    ProjectNotFoundError,
    GitHubError,
)

REMAINING = 200


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
                except NoMoreTokensError:
                    logger.critical("No more tokens")
                    self._handle_wait_time()
                    continue
                self.rate_limit_handling(func, *args, **kwargs)

    def update_token(self, new_token: str):
        self.token = new_token
        self.headers["Authorization"] = f"token {self.token}"

    def _handle_no_more_calls(self):
        tokens = self.tokens_handler.get_public_tokens(only_token=False)
        for token, calls, _ in tokens:
            if calls > REMAINING:
                logger.warning(f"Token changed {token[-10:]}")
                self.update_token(token)
                return
        logger.warning("No more tokens available")
        raise NoMoreTokensError("No more tokens available")

    def _handle_wait_time(self):
        token, calls, reset_time = self.tokens_handler.get_token_lowest_wait_time()
        now = datetime.now()
        wait_time = reset_time - now.timestamp()
        pprint(
            {
                "token": token[-10:],
                "calls": calls,
                "reset_time": reset_time,
                "now": now.timestamp(),
                "wait_time": wait_time,
            }
        )
        if wait_time > 0 and calls <= REMAINING:
            logger.warning(
                f"Waiting {wait_time} seconds  {now + timedelta(seconds=wait_time)}"
            )
            time.sleep(wait_time)
        self.update_token(token)

    def get(
        self,
        url,
        params=None,
        name: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
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
            remaining_limit = int(response.headers["X-RateLimit-Remaining"])
            if remaining_limit < REMAINING:
                raise RateLimitExceededError("GitHub API rate limit is low.")

            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            if (
                e.response.status_code == 403
                and "X-RateLimit-Remaining" in e.response.headers
                and int(e.response.headers["X-RateLimit-Remaining"]) <= REMAINING
            ):
                raise RateLimitExceededError("GitHub API rate limit exceeded.")
            elif e.response.status_code == 451:
                logger.exception("Proyecto eliminado", traceback=True)
                ProjectNotFoundError("Proyecto eliminado")
            elif e.response.status_code == 404:
                logger.exception("Proyecto no encontrado", traceback=True)
                ProjectNotFoundError("Proyecto no encontrado")
            elif e.response.status_code == 502:
                logger.exception("Error de GitHub", traceback=True)
                GitHubError("Error de GitHub")
                time.sleep(10)
                self.get(url, params=params, name=name)

            else:
                raise e

    def _realizar_solicitud_paginada(
        self,
        name: str,
        url: Union[str, None],
        params: Optional[Dict] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        if params is None:
            params = {}
        if headers is None:
            headers = self.headers

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
