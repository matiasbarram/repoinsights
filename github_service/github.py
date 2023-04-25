import requests
from datetime import datetime
from typing import Optional, Dict, Any, List, Set
import json
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
from .utils.utils import gh_api_to_datetime


class GitHubExtractor:
    def __init__(self, usuario, repositorio, token):
        self.usuario = usuario
        self.repositorio = repositorio
        self.token = token
        self.user_cache = {}
        self.commit_cache = {}
        self.repo = self.obtener_repositorio()

    def obtener_repositorio(self) -> Dict[str, Any]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repo = response.json()
        owner_name = repo["owner"]["login"]
        owner_data = self.obtener_usuario(owner_name)
        repo["owner"] = owner_data
        return repo

    def obtener_usuario(self, usuario: str) -> Dict[str, Any]:
        if usuario in self.user_cache:
            logger.debug("Getting usuario cacheado {commit_sha}", commit_sha=usuario)
            return self.user_cache[usuario]

        url = f"https://api.github.com/users/{usuario}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        user_data = response.json()
        self.user_cache[usuario] = user_data
        return user_data

    def _realizar_solicitud_paginada(self, name, url, params=None):
        if params is None:
            params = {}
        params.setdefault("per_page", 100)

        headers = {"Authorization": f"token {self.token}"}
        elementos = []
        pag = 1
        while url:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            elementos.extend(response.json())
            logger.info(f"{name} Pagina {pag}: {len(response.json())} elementos")
            pag += 1
            if "next" in response.links:
                url = response.links["next"]["url"]
            else:
                url = None
        return elementos

    def _realizar_solicitud_paginada_filtered(
        self, name, url, params=None, since=None, until=None
    ):
        if params is None:
            params = {}
        params.setdefault("per_page", 100)

        headers = {"Authorization": f"token {self.token}"}
        elementos = []
        pag = 1
        while url:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
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

        pull_requests = self._realizar_solicitud_paginada("PR", url, params)
        prs_filtradas = self._filtrar_por_fecha(pull_requests, since, until)

        users = self._get_users_for_keys(
            prs_filtradas,
            [
                "user",
                "head.user",
                "base.user",
                "head.repo.owner",
                "base.repo.owner",
            ],
        )
        self._add_users_to_dict_keys(
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

    def obtener_issues(
        self, since: Optional[datetime] = None, until: Optional[datetime] = None
    ):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/issues"
        params = {"state": "all", "per_page": 100, "since": since}
        issues = self._realizar_solicitud_paginada("Issue", url, params)
        return self._filtrar_por_fecha(issues, since, until)

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
        return {user: self.obtener_usuario(user) for user in users_to_fetch}

    def obtener_commits(
        self, since: Optional[datetime] = None, until: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits"
        params = {"since": since, "until": until, "per_page": 100}
        commits = self._realizar_solicitud_paginada("commit", url, params)
        users = self._get_users_for_keys(commits, ["author", "committer"])
        self._add_users_to_dict_keys(commits, users, ["author", "committer"])
        return commits

    def obtener_commit(self, commit_sha: str) -> Dict[str, Any]:
        if commit_sha in self.commit_cache:
            logger.debug("Getting commit cacheado {commit_sha}", commit_sha=commit_sha)
            return self.commit_cache[commit_sha]

        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits/{commit_sha}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        commit = response.json()
        users = self._get_users_for_keys([commit], ["author", "committer"])
        self._add_users_to_dict_keys([commit], users, ["author", "committer"])
        self.commit_cache[commit_sha] = commit
        return commit

    def obtener_contribuidores(self):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/contributors"
        params = {"per_page": 100}
        contribuidores = self._realizar_solicitud_paginada("contributors", url, params)
        return contribuidores

    def obtener_watchers(self):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/subscribers"
        params = {"per_page": 100}
        watchers = self._realizar_solicitud_paginada("watchers", url, params)
        return watchers
