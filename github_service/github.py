import concurrent.futures
import requests
from datetime import datetime
from typing import Optional, Dict, Any, List, Set
import json
from loguru import logger


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

    def _realizar_solicitud_paginada(self, name, url, params=None):
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
            logger.info(f"{name} Pagina {pag}: {len(response.json())} elementos")
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
        self,
        state: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[str] = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/pulls"
        params = {"per_page": 100, "since": since}
        if state:
            params["state"] = state
        if sort:
            params["sort"] = sort
        if direction:
            params["direction"] = direction

        pull_requests = self._realizar_solicitud_paginada("PR", url, params)
        prs_filtradas = self._filtrar_por_fecha(pull_requests, since, until)

        users_to_fetch = self._get_unique_users(prs_filtradas, "user")
        users_to_fetch.update(self._get_unique_users(prs_filtradas, "head.user"))
        users_to_fetch.update(self._get_unique_users(prs_filtradas, "base.user"))
        users_to_fetch.update(self._get_unique_users(prs_filtradas, "head.repo.owner"))
        users_to_fetch.update(self._get_unique_users(prs_filtradas, "base.repo.owner"))

        users = {user: self.obtener_usuario(user) for user in users_to_fetch}
        logger.info("Usuarios PRs: {len_users}", len_users=len(users))

        self._add_users_to_elements(prs_filtradas, users, "user")
        self._add_users_to_elements(prs_filtradas, users, "head.user")
        self._add_users_to_elements(prs_filtradas, users, "base.user")
        self._add_users_to_elements(prs_filtradas, users, "head.repo.owner")
        self._add_users_to_elements(prs_filtradas, users, "base.repo.owner")
        print("Pull Requests: ", json.dumps(prs_filtradas[-1]))

        return prs_filtradas

    def obtener_issues(
        self, since: Optional[datetime] = None, until: Optional[datetime] = None
    ):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/issues"
        params = {"state": "all", "per_page": 100, "since": since}
        issues = self._realizar_solicitud_paginada("Issue", url, params)
        return self._filtrar_por_fecha(issues, since, until)

    def _get_unique_users(self, elements, user_key: str) -> Set[str]:
        users_to_fetch = set()
        for element in elements:
            keys = user_key.split(".")
            user_obj = element
            for key in keys:
                if user_obj is not None:
                    user_obj = user_obj.get(key)
                else:
                    break
            if user_obj is not None:
                users_to_fetch.add(user_obj["login"])
        return users_to_fetch

    def _add_users_to_elements(self, elements, users, user_key: str):
        for element in elements:
            keys = user_key.split(".")
            user_obj = element
            for key in keys[:-1]:
                if user_obj is not None:
                    user_obj = user_obj.get(key)
                else:
                    break
            if user_obj is not None:
                last_key = keys[-1]
                if user_obj[last_key] is not None:
                    user_obj[last_key] = users[user_obj[last_key]["login"]]

    def _get_unique_users_multiple_keys(
        self, elements, user_keys: List[str]
    ) -> Set[str]:
        users_to_fetch = set()
        for user_key in user_keys:
            users_to_fetch.update(self._get_unique_users(elements, user_key))
        return users_to_fetch

    def _get_unique_users_nested(self, elements, user_keys: List[str]) -> Set[str]:
        users_to_fetch = set()
        for element in elements:
            current = element
            for key in user_keys:
                if current is not None:
                    current = current.get(key, None)
            if current is not None and "login" in current:
                users_to_fetch.add(current["login"])
        return users_to_fetch

    def _add_users_to_nested_elements(self, elements, users, user_keys: List[str]):
        for element in elements:
            current = element
            for i, key in enumerate(user_keys):
                if current is not None:
                    if i == len(user_keys) - 1:
                        if current[key] is not None and "login" in current[key]:
                            current[key] = users[current[key]["login"]]
                    else:
                        current = current.get(key, None)

    def obtener_commits(
        self, since: Optional[datetime] = None, until: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits"
        params = {"since": since, "until": until, "per_page": 100}
        commits = self._realizar_solicitud_paginada("commit", url, params)
        users_to_fetch = self._get_unique_users_multiple_keys(
            commits, ["author", "committer"]
        )
        users = {user: self.obtener_usuario(user) for user in users_to_fetch}
        self._add_users_to_elements(commits, users, "author")
        self._add_users_to_elements(commits, users, "committer")
        return commits

    def obtener_commit(self, commit_sha: str) -> Dict[str, Any]:
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits/{commit_sha}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        commit = response.json()
        users_to_fetch = self._get_unique_users_multiple_keys(
            [commit], ["author", "committer"]
        )
        users = {user: self.obtener_usuario(user) for user in users_to_fetch}
        logger.info("Usuarios commits: {len_users}", len_users=len(users))
        self._add_users_to_elements([commit], users, "author")
        self._add_users_to_elements([commit], users, "committer")
        return commit

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
        contribuidores = self._realizar_solicitud_paginada("contributors", url, params)
        return contribuidores

    def obtener_watchers(self):
        url = f"https://api.github.com/repos/{self.usuario}/{self.repositorio}/subscribers"
        params = {"per_page": 100}
        watchers = self._realizar_solicitud_paginada("watchers", url, params)
        return watchers
