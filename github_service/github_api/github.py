import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class GitHubRepo:
    def __init__(self, usuario, repositorio, token):
        self.usuario = usuario
        self.repositorio = repositorio
        self.token = token

    def _realizar_solicitud_paginada(self, url, params=None):
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

    def obtener_commits(
        self, since: Optional[datetime] = None, until: Optional[datetime] = None
    ):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits"
        params = {"since": since, "until": until, "per_page": 100}
        self.contar_elementos(url, params)
        commits = self._realizar_solicitud_paginada(url, params)
        return commits

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


if __name__ == "__main__":
    usuario = "akka"
    repositorio = "akka"
    token = "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"

    repo = GitHubRepo(usuario, repositorio, token)

    since = datetime(2022, 1, 10)
    until = datetime(2022, 2, 20)

    commits = repo.obtener_commits(since=since, until=until)
    pull_requests = repo.obtener_pull_requests(since=since, until=until)
    print("\nCommits:")
    print(f"Total: {len(commits)}")
