from datetime import datetime
from github import Issue, IssueComment, IssueEvent
from helper.utils import format_dt
from .repository import GHRepository


class GHIssue(GHRepository):
    def get_issues(self):
        issues = self.repo.get_issues(state="all", sort="created")
        return issues

    def get_issue_data(self, issue: Issue.Issue):
        reporter_id = issue.user.id if issue.user is not None else None
        assignee_id = issue.assignee.id if issue.assignee is not None else None
        is_pull_request = issue.pull_request is not None
        pull_request_id = None
        if is_pull_request:
            pass
            # pull_request_id = issue.pull_request  # Crear PR en DB y obtener el ID
        # TODO if is pull request get data, save and get ID
        print({"test": {"issue_title": issue.title, "issue_id": issue.number}})
        data = {
            "repo_id": self.repo.id,
            "reporter_id": reporter_id,
            "assignee_id": assignee_id,
            "issue_id": issue.number,
            "pull_request": is_pull_request,
            "pull_request_id": pull_request_id,  # Crear PR en DB y obtener el ID
            "created_at": format_dt(issue.created_at),
        }

        print(f"issue data {data}")
        return data

    def get_issue_comments(self, issue: Issue.Issue):
        comments = issue.get_comments()
        return comments

    def get_issue_comment_data(
        self, issue: Issue.Issue, comment: IssueComment.IssueComment
    ):
        data = {
            "id": comment.id,
            "user_id": comment.user.id,  # GET ID FROM DB
            "issue_id": issue.id,  # GET ID FROM DB
            "created_at": format_dt(comment.created_at),
            "updated_at": format_dt(comment.updated_at),
            "body": comment.body,
        }
        print(f"comment data {data}")
        return data

    def get_issue_events(self, issue: Issue.Issue):
        events = issue.get_events()
        return events

    def get_issue_event_data(self, issue: Issue.Issue, event: IssueEvent.IssueEvent):
        actor_id = event.actor.id if event.actor is not None else None
        data = {
            "event_id": event.id,
            "action_specific": None,  # TODO saber que es.
            "created_at": format_dt(event.created_at),
            "issue_id": issue.id,  # GET ID FROM DB
            "actor_id": actor_id,  # GET ID FROM DB
            "action": event.event,
        }
        print(f"event data {data}")
        return data
