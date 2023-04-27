from typing import Optional, Dict, Any, List, Set, Iterator
from extract_service.github_api.user import Repository, Commit, User
from extract_service.github_api.issue import Issue
from extract_service.github_api.pull_request import PullRequest
from extract_service.github_api.github_api import GitHubAPI
from datetime import datetime


class GitHubExtractor:
    def __init__(
        self,
        usuario: str,
        repositorio: str,
        tokens_iter: Iterator[str],
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ):
        self.usuario = usuario
        self.since = since
        self.until = until
        token = next(tokens_iter)
        self.tokens_iter = tokens_iter
        self.api = GitHubAPI(token)

        self.repositorio = Repository(self.api, repositorio, usuario, self.tokens_iter)
        self.user_repo = User(self.api, tokens_iter)
        self.commit_repo = Commit(self.api, usuario, repositorio, tokens_iter)
        self.issue = Issue(token, usuario, repositorio, tokens_iter)
        self.pull_request = PullRequest(self.api, usuario, repositorio, tokens_iter)

    def obtener_repo_info(self):
        return self.repositorio.obtener_repositorio()

    def obtener_contribuidores(self):
        return self.repositorio.obtener_contribuidores()

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

    def obtener_stargazers(self):
        return self.repositorio.obtener_stargazers()
