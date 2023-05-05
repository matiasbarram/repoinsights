from typing import Any, Dict
from extract_service.repoinsights.user import InsightsUser


class InsightsMilestone:
    def __init__(self, milestone: Dict[str, Any]):
        self.id = milestone["id"]
        self.name = milestone["title"]
        self.description = milestone["description"]
        self.state = milestone["state"]
        self.created_at = milestone["created_at"]
        self.updated_at = milestone["updated_at"]
        self.due_on = milestone["due_on"]
        self.creator = InsightsUser(milestone["creator"])

    def set_repo_id(self, repo_id: int):
        self.repo_id = repo_id

    def to_dict(self):
        return {
            "id": self.id,
            "repo_id": self.repo_id,
            "name": self.name,
        }
