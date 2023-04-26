from datetime import datetime
from typing import Any, Dict, List, Optional
from .github_api import GitHubAPI, GitHubResource
from .user import User
from ..utils.utils import add_users_to_dict_keys
from .user import User
from ..utils.utils import add_users_to_dict_keys


class Issue(GitHubResource):
    def __init__(self, token, usuario, repositorio, tokens_iter) -> None:
        self.usuario = usuario
        self.repositorio = repositorio
        self.tokens_iter = tokens_iter
        self.api = GitHubAPI(token)

    def obtener_issues(
        self,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        state: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/issues"
        params = {"state": "all", "per_page": 100, "since": since}

        issues = self.invoke_with_rate_limit_handling(
            self.api.get,
            url=url,
            params=params,
            tokens_iter=self.tokens_iter,
        ).json()

        issues_filtrados = self.api._filtrar_por_fecha(issues, since, until)
        users = User(self.api, self.tokens_iter)._get_users_for_keys(
            issues_filtrados, ["user", "assignee"]
        )
        add_users_to_dict_keys(issues_filtrados, users, ["user", "assignee"])
        return issues_filtrados
