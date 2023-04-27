from github.Milestone import Milestone


class InsightsMilestone:
    def __init__(self, milestone: Milestone):
        self.id = milestone.id
        self.title = milestone.title
        self.description = milestone.description
        self.state = milestone.state
        self.created_at = milestone.created_at
        self.updated_at = milestone.updated_at
        self.due_on = milestone.due_on
        self.creator = milestone.creator.login

    def __str__(self):
        return f"Milestone {self.title} ({self.state})"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "state": self.state,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "due_on": self.due_on,
            "creator": self.creator,
        }
