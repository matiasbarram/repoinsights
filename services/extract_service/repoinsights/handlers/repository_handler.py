from ...github_api.extractor import GitHubExtractor
from typing import Dict, Any


class InsightsRepositoryHandler:
    def __init__(self, repo: GitHubExtractor) -> None:
        self.repo = repo

    def get_repo_info(self) -> Dict[str, Any]:
        return self.repo.obtener_repo_info()
