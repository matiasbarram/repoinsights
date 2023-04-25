from extract_service.github_api.github_api import GitHubAPI, GitHubResource
from typing import Optional, Dict, Any, List, Set, Iterator
from loguru import logger
from datetime import datetime
from ..utils.utils import get_unique_users, add_users_to_dict_keys
from .github_api import Cache


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
        super().__init__(self.api)

    def obtener_usuario(self, usuario: str) -> Dict[str, Any]:
        if self.cache.has(usuario):
            logger.debug("Getting usuario cacheado {commit_sha}", commit_sha=usuario)
            return self.cache.get(usuario)  # type: ignore

        url = f"https://api.github.com/users/{usuario}"
        user_data = self.api.get(url).json()
        self.cache.set(usuario, user_data)
        return user_data

    def _get_users_for_keys(
        self, elements, user_keys: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        users_to_fetch = set()
        for user_key in user_keys:
            users_to_fetch.update(get_unique_users(elements, user_key))
        return {user: self.obtener_usuario(user) for user in users_to_fetch}


class Commit(GitHubResource):
    def __init__(self, api: GitHubAPI, usuario: str, repositorio: str):
        self.api = api
        self.usuario = usuario
        self.repositorio = repositorio
        super().__init__(self.api)

    def obtener_commit(self, commit_sha: str) -> Dict[str, Any]:
        if self.cache.has(commit_sha):
            logger.debug("Getting commit cacheado {commit_sha}", commit_sha=commit_sha)
            return self.cache.get(commit_sha)  # type: ignore

        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits/{commit_sha}"
        commit = self.api.get(url).json()
        users = User(self.api)._get_users_for_keys([commit], ["author", "committer"])
        add_users_to_dict_keys([commit], users, ["author", "committer"])
        self.cache.set(commit_sha, commit)
        return commit

    def obtener_commits(
        self, since: Optional[datetime] = None, until: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits"
        params = {"since": since, "until": until, "per_page": 100}
        commits = self.api._realizar_solicitud_paginada("commit", url, params)
        users = User(self.api)._get_users_for_keys(commits, ["author", "committer"])
        add_users_to_dict_keys(commits, users, ["author", "committer"])
        return commits
