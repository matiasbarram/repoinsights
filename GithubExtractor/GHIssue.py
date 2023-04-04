from datetime import datetime
from github import Issue, IssueComment
from helper.utils import format_dt


class GHIssue:
    def get_issues(self):
        issues = self.repo.get_issues(state="all")
        return issues

    def get_issue_data(self, issue: Issue.Issue):
        reporter_id = issue.user.id if issue.user is not None else None
        assignee_id = issue.assignee.id if issue.assignee is not None else None
        # pull_request_id = issue.pull_request.id if issue.pull_request is not None else None # Crear PR en DB y obtener el ID
        # TODO if is pull request get data, save and get ID
        print(reporter_id)
        data = {
            "repo_id": self.repo.id,
            "reporter_id": reporter_id,
            "assignee_id": assignee_id,
            "issue_id": issue.id,
            "pull_request": issue.pull_request,
            "pull_request_id": None,  # Crear PR en DB y obtener el ID
            "created_at": format_dt(issue.created_at),
        }

        # print(f"issue data {data}")
        # return data

    def get_issue_comments(self, issue: Issue.Issue):
        comments = issue.get_comments()
        return comments

    def get_issue_comment_data(self, comment: IssueComment.IssueComment):
        data = {
            "id": comment.id,
            "user_id": comment.user.id,
            "issue_id": comment.issue.id,
            "created_at": format_dt(comment.created_at),
            "updated_at": format_dt(comment.updated_at),
            "body": comment.body,
        }
        print(f"comment data {data}")
        return data
