import concurrent.futures
import requests
from datetime import datetime
from typing import Optional, Dict, Any, List


class GitHubExtractor:
    def __init__(self, usuario, repositorio, token):
        self.usuario = usuario
        self.repositorio = repositorio
        self.token = token
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
        url = f"https://api.github.com/users/{usuario}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def _realizar_solicitud_paginada(self, url, params=None):
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
            print(f"Pagina {pag}: {len(response.json())} elementos")
            pag += 1
            if "next" in response.links:
                url = response.links["next"]["url"]
            else:
                url = None

        return elementos

    def _filtrar_por_fecha(self, elementos, since=None, until=None):
        if since:
            since = datetime.fromisoformat(since)
        if until:
            until = datetime.fromisoformat(until)

        resultados = []
        for elemento in elementos:
            created_at = datetime.fromisoformat(
                elemento["created_at"].replace("Z", "+00:00")
            )

            if since and created_at < since:
                continue

            if until and created_at > until:
                continue

            resultados.append(elemento)

        return resultados

    def obtener_pull_requests(
        self, since: Optional[datetime] = None, until: Optional[datetime] = None
    ):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/pulls"
        params = {"state": "all", "per_page": 100, "since": since}
        pull_requests = self._realizar_solicitud_paginada(url, params)
        return self._filtrar_por_fecha(pull_requests, since, until)

    def obtener_issues(
        self, since: Optional[datetime] = None, until: Optional[datetime] = None
    ):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/issues"
        params = {"state": "all", "per_page": 100, "since": since}
        issues = self._realizar_solicitud_paginada(url, params)
        return self._filtrar_por_fecha(issues, since, until)

    def obtener_usuario_parallel(self, usuario: str) -> Dict[str, Any]:
        return usuario, self.obtener_usuario(usuario)  # type: ignore

    def obtener_commits(
        self, since: Optional[datetime] = None, until: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits"
        params = {"since": since, "until": until, "per_page": 100}
        commits = self._realizar_solicitud_paginada(url, params)

        users_to_fetch = set()
        for commit in commits:
            if commit["author"] is not None:
                users_to_fetch.add(commit["author"]["login"])
            if commit["committer"] is not None:
                users_to_fetch.add(commit["committer"]["login"])
        users = {user: self.obtener_usuario(user) for user in users_to_fetch}

        for commit in commits:
            if commit["author"] is not None:
                commit["author"] = users[commit["author"]["login"]]
            if commit["committer"] is not None:
                commit["committer"] = users[commit["committer"]["login"]]

        return commits

    def obtener_commit(self, commit_sha: str) -> Dict[str, Any]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits/{commit_sha}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def contar_elementos(self, url, params: Dict[str, Any]):
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        if "last" in response.links:
            last_url = response.links["last"]["url"]
            last_page_number = int(last_url.split("=")[-1])
            return last_page_number * 100
        else:
            return len(response.json())

    def obtener_contribuidores(self):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/contributors"
        params = {"per_page": 100}
        contribuidores = self._realizar_solicitud_paginada(url, params)
        return contribuidores

    def obtener_watchers(self):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/subscribers"
        params = {"per_page": 100}
        watchers = self._realizar_solicitud_paginada(url, params)
        return watchers
