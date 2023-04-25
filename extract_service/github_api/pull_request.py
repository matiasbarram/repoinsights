from datetime import datetime
from typing import Any, Dict, List, Optional
from .github_api import GitHubAPI, GitHubResource
from .user import User
from loguru import logger
from ..utils.utils import add_users_to_dict_keys


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

        users = User(self.api)._get_users_for_keys(
            prs_filtradas,
            [
                "user",
                "head.user",
                "base.user",
                "head.repo.owner",
                "base.repo.owner",
            ],
        )
        add_users_to_dict_keys(
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
