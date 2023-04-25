import requests
from datetime import datetime
from typing import Optional, Dict, Any, List, Set, Iterator
import json
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
from ..utils.utils import gh_api_to_datetime
from functools import wraps


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

    def _add_users_to_dict_keys(
        self, list_dicts: List, users: Dict, user_keys: List[str]
    ):
        for dict in list_dicts:
            for key in user_keys:
                keys = key.split(".")
                user_obj = dict
                for k in keys[:-1]:
                    if user_obj is not None:
                        user_obj = user_obj.get(k)
                    else:
                        break
                if user_obj is not None:
                    last_key = keys[-1]
                    if user_obj[last_key] is not None:
                        user_obj[last_key] = users[user_obj[last_key]["login"]]

    def _get_unique_users(self, elements, user_key: str) -> Set[str]:
        users_to_fetch = set()
        for element in elements:
            keys = user_key.split(".")
            user_obj = element
            for key in keys:
                if user_obj is not None:
                    user_obj = user_obj.get(key)
                else:
                    break
            if user_obj is not None:
                users_to_fetch.add(user_obj["login"])
        return users_to_fetch

    def _get_users_for_keys(
        self, elements, user_keys: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        users_to_fetch = set()
        for user_key in user_keys:
            users_to_fetch.update(self._get_unique_users(elements, user_key))
        return {
            user: User(GitHubAPI(self.token)).obtener_usuario(user)
            for user in users_to_fetch
        }


class GitHubResource:
    def __init__(self, api: GitHubAPI):
        self.api = api

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


class Repository(GitHubResource):
    def __init__(self, api: GitHubAPI, repositorio, usuario) -> None:
        self.usuario = usuario
        self.repositorio = repositorio
        self.api = api

    def obtener_repositorio(self) -> Dict[str, Any]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}"
        repo = self.api.get(url).json()
        owner_name = repo["owner"]["login"]
        owner_data = User(self.api).obtener_usuario(owner_name)
        repo["owner"] = owner_data
        return repo

    def obtener_contribuidores(self):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/contributors"
        params = {"per_page": 100}
        contribuidores = self.api._realizar_solicitud_paginada(
            "contributors", url, params
        )
        return contribuidores

    def obtener_watchers(self):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/subscribers"
        params = {"per_page": 100}
        watchers = self.api._realizar_solicitud_paginada("watchers", url, params)
        return watchers

    def obtener_labels(self) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/labels"
        labels = self.api._realizar_solicitud_paginada("labels", url)
        return labels


class User(GitHubResource):
    def __init__(self, api: GitHubAPI):
        self.api = api
        self.user_cache = {}

    def obtener_usuario(self, usuario: str) -> Dict[str, Any]:
        if usuario in self.user_cache:
            logger.debug("Getting usuario cacheado {commit_sha}", commit_sha=usuario)
            return self.user_cache[usuario]

        url = f"https://api.github.com/users/{usuario}"
        user_data = self.api.get(url).json()
        self.user_cache[usuario] = user_data
        return user_data


class Commit(GitHubResource):
    def __init__(self, api: GitHubAPI, usuario: str, repositorio: str):
        self.api = api
        self.usuario = usuario
        self.repositorio = repositorio
        self.commit_cache = {}

    def obtener_commit(self, commit_sha: str) -> Dict[str, Any]:
        if commit_sha in self.commit_cache:
            logger.debug("Getting commit cacheado {commit_sha}", commit_sha=commit_sha)
            return self.commit_cache[commit_sha]

        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits/{commit_sha}"
        commit = self.api.get(url).json()
        self.commit_cache[commit_sha] = commit
        users = self.api._get_users_for_keys([commit], ["author", "committer"])
        self.api._add_users_to_dict_keys([commit], users, ["author", "committer"])
        self.commit_cache[commit_sha] = commit
        return commit

    def obtener_commits(
        self, since: Optional[datetime] = None, until: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits"
        params = {"since": since, "until": until, "per_page": 100}
        commits = self.api._realizar_solicitud_paginada("commit", url, params)
        users = self.api._get_users_for_keys(commits, ["author", "committer"])
        self.api._add_users_to_dict_keys(commits, users, ["author", "committer"])
        return commits


class Issue(GitHubResource):
    def __init__(self, token, usuario, repositorio) -> None:
        self.usuario = usuario
        self.repositorio = repositorio
        self.api = GitHubAPI(token)

    def obtener_issues(
        self,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        state: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/issues"
        params = {"state": "all", "per_page": 100, "since": since}

        issues = self.api._realizar_solicitud_paginada("Issue", url, params)
        issues_filtrados = self.api._filtrar_por_fecha(issues, since, until)
        users = self.api._get_users_for_keys(issues_filtrados, ["user", "assignee"])
        self.api._add_users_to_dict_keys(issues_filtrados, users, ["user", "assignee"])
        return issues_filtrados


class PullRequest(GitHubResource):
    def __init__(self, api: GitHubAPI, usuario, repositorio) -> None:
        self.api = api
        self.usuario = usuario
        self.repositorio = repositorio

    def obtener_pull_requests(
        self,
        state: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[str] = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/pulls"
        params = {"per_page": 100, "since": since}
        if state:
            params["state"] = state
        if sort:
            params["sort"] = sort
        if direction:
            params["direction"] = direction

        pull_requests = self.api._realizar_solicitud_paginada("PR", url, params)
        prs_filtradas = self.api._filtrar_por_fecha(pull_requests, since, until)

        users = self.api._get_users_for_keys(
            prs_filtradas,
            [
                "user",
                "head.user",
                "base.user",
                "head.repo.owner",
                "base.repo.owner",
            ],
        )
        self.api._add_users_to_dict_keys(
            prs_filtradas,
            users,
            [
                "user",
                "head.user",
                "base.user",
                "head.repo.owner",
                "base.repo.owner",
            ],
        )
        logger.info("PRs filtradas: {prs}", prs=len(prs_filtradas))

        return prs_filtradas


class GitHubExtractor:
    def __init__(self, usuario: str, repositorio: str, tokens_iter: Iterator[str]):
        self.usuario = usuario
        token = next(tokens_iter)
        self.tokens_iter = tokens_iter
        self.api = GitHubAPI(token)

        self.repositorio = Repository(self.api, repositorio, usuario)
        self.repo = self.obtener_repo_info()

        self.user_repo = User(self.api)
        self.commit_repo = Commit(self.api, usuario, repositorio)
        self.issue = Issue(token, usuario, repositorio)
        self.pull_request = PullRequest(self.api, usuario, repositorio)

    def obtener_repo_info(self):
        return self.repositorio.obtener_repositorio()

    def obtener_contribuidores(self):
        return self.repositorio.obtener_contribuidores()

    def obtener_watchers(self):
        return self.repositorio.obtener_watchers()

    def obtener_usuario(self, usuario):
        return self.user_repo.obtener_usuario(usuario)

    def obtener_commit(self, commit_sha):
        return self.commit_repo.obtener_commit(commit_sha)

    def obtener_commits(self, since=None, until=None):
        return self.commit_repo.obtener_commits(since=since, until=until)

    def obtener_issues(self, since=None, until=None, state=None):
        return self.issue.obtener_issues(since=since, until=until, state=state)

    def obtener_pull_requests(
        self, state=None, sort=None, direction=None, since=None, until=None
    ):
        return self.pull_request.obtener_pull_requests(
            state=state, sort=sort, direction=direction, since=since, until=until
        )

    def obtener_labels(self):
        return self.repositorio.obtener_labels()
