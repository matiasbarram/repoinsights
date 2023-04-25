import requests
from loguru import logger
from ..utils.utils import gh_api_to_datetime
from typing import Optional, Dict, Any, List, Set, Iterator
from ..utils.utils import get_unique_users, add_users_to_dict_keys


class RateLimitExceededError(Exception):
    pass


class GitHubAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": f"token {self.token}"}

    def update_token(self, new_token):
        self.token = new_token
        self.headers["Authorization"] = f"token {self.token}"

    def get(self, url, params=None):
        try:
            response = requests.get(url, headers=self.headers, params=params)
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

    def _realizar_solicitud_paginada(self, name, url, params=None):
        if params is None:
            params = {}
        params.setdefault("per_page", 100)

        elementos = []
        pag = 1
        while url:
            response = self.get(url, params=params)
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
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def has(self, key):
        return key in self.cache


class GitHubResource:
    def __init__(self, api: GitHubAPI):
        self.api = api
        self.cache = Cache()

    def _handle_rate_limit_exceeded(self, tokens_iter):
        try:
            new_token = next(tokens_iter)
            self.api.update_token(new_token)
        except StopIteration:
            raise RateLimitExceededError(
                "GitHub API rate limit exceeded and no more tokens available."
            )

    def invoke_with_rate_limit_handling(self, func, tokens_iter, *args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except RateLimitExceededError:
                self._handle_rate_limit_exceeded(tokens_iter)
