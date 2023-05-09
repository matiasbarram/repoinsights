import json
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
        params = {"per_page": 100}
        if state:
            params["state"] = state  # type: ignore
        if since:
            params["since"] = since  # type: ignore

        issues = self.invoke_with_rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            name="issues",
            url=url,
            params=params,
            tokens_iter=self.tokens_iter,
        )

        issues_filtrados = self.api._filtrar_por_fecha(issues, since, until)
        users = User(self.api, self.tokens_iter)._get_users_for_keys(
            issues_filtrados, ["user", "assignee"]
        )
        add_users_to_dict_keys(issues_filtrados, users, ["user", "assignee"])
        return issues_filtrados

    def obtener_issues_comments(self) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/issues/comments"
        params = {"per_page": 100}
        issues_comments = self.invoke_with_rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            name="issues_comments",
            url=url,
            params=params,
            tokens_iter=self.tokens_iter,
        )
        users = User(self.api, self.tokens_iter)._get_users_for_keys(
            issues_comments, ["user"]
        )
        add_users_to_dict_keys(issues_comments, users, ["user"])
        return issues_comments

    def obtener_issue_events(self, issue_id) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/issues/{issue_id}/events"
        params = {"per_page": 100}
        issues_events = self.invoke_with_rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            name=f"issues_events de {issue_id}",
            url=url,
            params=params,
            tokens_iter=self.tokens_iter,
        )
        users = User(self.api, self.tokens_iter)._get_users_for_keys(
            issues_events, ["actor"]
        )
        add_users_to_dict_keys(issues_events, users, ["actor"])
        return issues_events

    def obtener_issues_events(self) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/issues/events"
        params = {"per_page": 100}
        issues_events = self.invoke_with_rate_limit_handling(
            self.api._realizar_solicitud_paginada,
            name="issues_events",
            url=url,
            params=params,
            tokens_iter=self.tokens_iter,
        )
        users = User(self.api, self.tokens_iter)._get_users_for_keys(
            issues_events, ["actor"]
        )
        add_users_to_dict_keys(issues_events, users, ["actor"])
        return issues_events