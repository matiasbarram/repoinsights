from datetime import datetime
from github.Repository import Repository
from github.Issue import Issue
from .comment import GHIssueComment
from .label import GHLabel


class GHIssue:
    def __init__(self, issue: Issue) -> None:
        self.id = issue.id
        self.reporter_id = issue.assignee
        self.pull_request = issue.pull_request
        self.pull_request_id = issue.id
        self.created_at = issue.closed_by
        self.updated_at = issue.updated_at
        self.closed_at = issue.closed_at
        self.title = issue.title
        self.state = issue.state
        self.labels = []

    def set_labels(self, labels):
        self.labels = [GHLabel(label) for label in labels]

    def get_labels(self):
        print("Getting labels")
        return self.labels

    def set_comments(self, comments: list[GHIssueComment]):
        self.comments = comments

    def get_comments(self) -> list[GHIssueComment]:
        return self.comments

    #     print(f"issue data {data}")
    #     return data

    # def get_issue_comments(self, issue: Issue.Issue):
    #     comments = issue.get_comments()
    #     return comments

    # def get_issue_comment_data(
    #     self, issue: Issue.Issue, comment: IssueComment.IssueComment
    # ):
    #     data = {
    #         "id": comment.id,
    #         "user_id": comment.user.id,  # GET ID FROM DB
    #         "issue_id": issue.id,  # GET ID FROM DB
    #         "created_at": format_dt(comment.created_at),
    #         "updated_at": format_dt(comment.updated_at),
    #         "body": comment.body,
    #     }
    #     print(f"comment data {data}")
    #     return data

    # def get_issue_events(self, issue: Issue.Issue):
    #     events = issue.get_events()
    #     return events

    # def get_issue_event_data(self, issue: Issue.Issue, event: IssueEvent.IssueEvent):
    #     actor_id = event.actor.id if event.actor is not None else None
    #     data = {
    #         "event_id": event.id,
    #         "action_specific": None,  # TODO saber que es.
    #         "created_at": format_dt(event.created_at),
    #         "issue_id": issue.id,  # GET ID FROM DB
    #         "actor_id": actor_id,  # GET ID FROM DB
    #         "action": event.event,
    #     }
    #     print(f"event data {data}")
    #     return data
