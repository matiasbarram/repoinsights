from extract_service.github_api.github_api import GitHubAPI, GitHubResource
from typing import Optional, Dict, Any, List, Set, Iterator, Union
from loguru import logger
from datetime import datetime
from ..utils.utils import get_unique_users, add_users_to_dict_keys
from .github_api import Cache


class GitHubUserException(Exception):
    pass


class Repository(GitHubResource):
    def __init__(self, api: GitHubAPI, repositorio, usuario, tokens_iter) -> None:
        self.usuario = usuario
        self.repositorio = repositorio
        self.api = api
        self.tokens_iter = tokens_iter
        super().__init__(api)

    def obtener_repositorio(self) -> Dict[str, Any]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}"
        # repo = self.api.get(url).json()
        repo = self.invoke_with_rate_limit_handling(
            self.api.get, self.tokens_iter, url=url
        ).json()
        owner_name = repo["owner"]["login"]
        owner_data = User(self.api, self.tokens_iter).obtener_usuario(owner_name)
        repo["owner"] = owner_data
        return repo

    def obtener_contribuidores(self):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/contributors"
        params = {"per_page": 100}
        # contribuidores = self.api._realizar_solicitud_paginada(
        #     "contributors", url, params
        # )
        contribuidores = self.invoke_with_rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            self.tokens_iter,
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
            "stargazers", url, headers=headers
        )
        for stargazer in stargazers:
            user_name = stargazer["user"]["login"]
            user_data = User(self.api, self.tokens_iter).obtener_usuario(user_name)
            stargazer["user"] = user_data

        return stargazers

    def obtener_labels(self) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/labels"
        labels = self.invoke_with_rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            self.tokens_iter,
            url=url,
            name="labels",
        )
        return labels


class User(GitHubResource):
    def __init__(self, api: GitHubAPI, tokens_iter):
        self.api = api
        self.tokens_iter = tokens_iter
        super().__init__(self.api)

    def obtener_usuario(self, usuario: str) -> Union[Dict[str, Any], None]:
        if self.cache.has(usuario):
            logger.debug("Getting usuario cacheado {commit_sha}", commit_sha=usuario)
            return self.cache.get(usuario)  # type: ignore

        url = f"https://api.github.com/users/{usuario}"
        try:
            user_data = self.invoke_with_rate_limit_handling(
                self.api.get, self.tokens_iter, url=url
            ).json()

            self.cache.set(usuario, user_data)
            return user_data
        except Exception as e:
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

        # return {user: self.obtener_usuario(user) for user in users_to_fetch}


class Commit(GitHubResource):
    def __init__(self, api: GitHubAPI, usuario: str, repositorio: str, tokens_iter):
        self.api = api
        self.usuario = usuario
        self.repositorio = repositorio
        self.tokens_iter = tokens_iter
        super().__init__(self.api)

    def obtener_commit(self, commit_sha: str) -> Dict[str, Any]:
        if self.cache.has(commit_sha):
            logger.debug("Getting commit cacheado {commit_sha}", commit_sha=commit_sha)
            return self.cache.get(commit_sha)  # type: ignore

        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits/{commit_sha}"
        commit = self.invoke_with_rate_limit_handling(
            self.api.get, self.tokens_iter, url=url
        ).json()

        users = User(self.api, self.tokens_iter)._get_users_for_keys(
            [commit], ["author", "committer"]
        )
        add_users_to_dict_keys([commit], users, ["author", "committer"])
        self.cache.set(commit_sha, commit)
        return commit

    def obtener_commits(
        self, since: Optional[datetime] = None, until: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits"
        params = {"since": since, "until": until, "per_page": 100}
        commits = self.invoke_with_rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            tokens_iter=self.tokens_iter,
            url=url,
            params=params,
            name="commits",
        )

        users = User(self.api, self.tokens_iter)._get_users_for_keys(
            commits, ["author", "committer"]
        )
        add_users_to_dict_keys(commits, users, ["author", "committer"])
        return commits
