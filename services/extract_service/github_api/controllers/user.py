from services.extract_service.github_api.github_api import GitHubAPI
from typing import Optional, Dict, Any, List, Set, Iterator, Union
from loguru import logger
from datetime import datetime
from ...utils.utils import get_unique_users, add_users_to_dict_keys
from ..github_api import Cache
from pprint import pprint


class GitHubUserException(Exception):
    pass


class Repository:
    def __init__(self, api: GitHubAPI, repositorio, usuario) -> None:
        self.usuario = usuario
        self.repositorio = repositorio
        self.api = api

    def obtener_repositorio(self) -> Dict[str, Any]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}"
        repo = self.api.invoke_with_rate_limit_handling(self.api.get, url=url).json()
        owner_name = repo["owner"]["login"]
        owner_data = User(self.api).obtener_usuario(owner_name)
        repo["owner"] = owner_data
        return repo

    def obtener_contribuidores(self):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/contributors"
        params = {"per_page": 100}
        contribuidores = self.api.invoke_with_rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            name="contributors",
            url=url,
            params=params,
        )
        return contribuidores

    def obtener_stargazers(self):
        url = (
            f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/stargazers"
        )
        headers = {"Accept": "application/vnd.github.v3.star+json"}
        stargazers = self.api._realizar_solicitud_paginada(
            name="stargazers", url=url, headers=headers
        )
        for stargazer in stargazers:
            user_name = stargazer["user"]["login"]
            user_data = User(self.api).obtener_usuario(user_name)
            stargazer["user"] = user_data

        return stargazers

    def obtener_labels(self) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/labels"
        labels = self.api.invoke_with_rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            url=url,
            name="labels",
        )
        return labels

    def obtener_milestone(self, state=None) -> List[Dict[str, Any]]:
        url = (
            f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/milestones"
        )
        params = {"state": state}
        milestone = self.api.invoke_with_rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            url=url,
            params=params,
            name="milestone",
        )
        users = User(self.api)._get_users_for_keys(
            milestone,
            ["creator"],
        )
        add_users_to_dict_keys(
            milestone,
            users,
            ["creator"],
        )
        return milestone


class User:
    def __init__(self, api: GitHubAPI):
        self.api = api

    def obtener_usuario(self, usuario: str) -> Union[Dict[str, Any], None]:
        if self.api.cache.has(usuario):
            logger.debug("Getting usuario cacheado {commit_sha}", commit_sha=usuario)
            return self.api.cache.get(usuario)  # type: ignore

        url = f"https://api.github.com/users/{usuario}"
        try:
            user_data = self.api.invoke_with_rate_limit_handling(
                self.api.get, url=url
            ).json()

            self.api.cache.set(usuario, user_data)
            return user_data
        except Exception:
            logger.error(f"Error al obtener usuario {usuario}")
            return None

    def _get_users_for_keys(
        self, elements, user_keys: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        users_to_fetch = set()
        for user_key in user_keys:
            users_to_fetch.update(get_unique_users(elements, user_key))
        users = {}
        for user in users_to_fetch:
            new_user = self.obtener_usuario(user)
            if new_user:
                users[user] = new_user
        return users


class Commit:
    def __init__(self, api: GitHubAPI, usuario: str, repositorio: str):
        self.api = api
        self.usuario = usuario
        self.repositorio = repositorio

    def obtener_commit(self, commit_sha: str) -> Dict[str, Any]:
        if self.api.cache.has(commit_sha):
            logger.debug("Getting commit cacheado {commit_sha}", commit_sha=commit_sha)
            return self.api.cache.get(commit_sha)  # type: ignore

        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits/{commit_sha}"
        commit = self.api.invoke_with_rate_limit_handling(self.api.get, url=url).json()

        users = User(self.api)._get_users_for_keys([commit], ["author", "committer"])
        add_users_to_dict_keys([commit], users, ["author", "committer"])
        self.api.cache.set(commit_sha, commit)
        return commit

    def obtener_commits(
        self, since: Optional[datetime] = None, until: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits"
        params = {"since": since, "until": until, "per_page": 100}
        commits = self.api.invoke_with_rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            url=url,
            params=params,
            name="commits",
        )

        users = User(self.api)._get_users_for_keys(commits, ["author", "committer"])
        add_users_to_dict_keys(commits, users, ["author", "committer"])
        return commits

    def obtener_comments(self) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/comments"
        params = {"per_page": 100}
        comments = self.api.invoke_with_rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            url=url,
            params=params,
            name="all commits comments",
        )
        if comments:
            users = User(self.api)._get_users_for_keys(comments, ["user"])
            add_users_to_dict_keys(comments, users, ["user"])
        return comments

    def obtener_commit_comments(self, commit: str) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits/{commit}/comments"
        params = {"per_page": 100}
        comments = self.api.invoke_with_rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            url=url,
            params=params,
            name=f"commit {commit} comments",
        )

        if comments:
            users = User(self.api)._get_users_for_keys(comments, ["user"])
            add_users_to_dict_keys(comments, users, ["user"])
        return comments
