from services.extract_service.extract_module.github_api.github_api import GitHubAPI
from typing import Optional, Dict, Any, List, Union
from loguru import logger
from datetime import datetime
from services.extract_service.utils.utils import (
    get_unique_users,
    add_users_to_dict_keys,
)


class Commit:
    def __init__(self, api: GitHubAPI, usuario: str, repositorio: str, user):
        self.api = api
        self.usuario = usuario
        self.repositorio = repositorio
        self.user_controller = user

    def obtener_commit(self, commit_sha: str) -> Dict[str, Any]:
        if self.api.cache.has(commit_sha):
            logger.debug("Getting commit cacheado {commit_sha}", commit_sha=commit_sha)
            return self.api.cache.get(commit_sha)  # type: ignore

        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits/{commit_sha}"
        commit = self.api.rate_limit_handling(self.api.get, url=url)
        if commit is None:
            raise Exception(f"Commit {commit_sha} not found")
        commit = commit.json()

        users = self.user_controller._get_users_for_keys(
            [commit], ["author", "committer"]
        )
        add_users_to_dict_keys([commit], users, ["author", "committer"])
        self.api.cache.set(commit_sha, commit)
        return commit

    def obtener_commits(
        self, since: Optional[datetime] = None, until: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits"
        params = {"since": since, "until": until, "per_page": 100}
        commits = self.api.rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            url=url,
            params=params,
            name="commits",
        )

        users = self.user_controller._get_users_for_keys(
            commits, ["author", "committer"]
        )
        add_users_to_dict_keys(commits, users, ["author", "committer"])
        return commits

    def obtener_comments(self) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/comments"
        params = {"per_page": 100}
        comments = self.api.rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            url=url,
            params=params,
            name="all commits comments",
        )
        if comments:
            users = self.user_controller._get_users_for_keys(comments, ["user"])
            add_users_to_dict_keys(comments, users, ["user"])
        return comments

    def obtener_commit_comments(self, commit: str) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits/{commit}/comments"
        params = {"per_page": 100}
        comments = self.api.rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            url=url,
            params=params,
            name=f"commit {commit} comments",
        )

        if comments:
            users = self.user_controller._get_users_for_keys(comments, ["user"])
            add_users_to_dict_keys(comments, users, ["user"])
        return comments
