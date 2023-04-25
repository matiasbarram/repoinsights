from github.IssueEvent import IssueEvent


class GHIssueEvent:
    def __init__(self, event: IssueEvent) -> None:
        self.event_id = event.id
        self.action_specific = None
        self.created_at = event.created_at
        self.issue_id = event.issue.id
        self.actor_id = event.actor.id
        self.actor = event.actor.login if event.actor else None
        self.action = event.event

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "action_specific": self.action_specific,
            "created_at": self.created_at,
            "issue_id": self.issue_id,
            "actor_id": self.actor_id,
            "actor": self.actor,
            "action": self.action,
        }
