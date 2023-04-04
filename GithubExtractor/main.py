from typing import Union
from helper.utils import format_dt, get_user_type
from pprint import pprint
from github import (
    Github,
    Repository,
    PullRequest,
    NamedUser,
    Commit,
    Issue,
    Label,
    Project,
    IssueComment,
)
import os
import json
import random
from typing import Union


class GHToken:
    def test_token(self, token) -> Union[Github, bool]:
        github_api = Github(token)
        try:
            me: str = github_api.get_user().login
            print(f"Hello! {me}")
            return github_api
        except Exception as e:
            return False

    def get_public_tokens(self, token: Union[str, None]) -> list:
        keys_list = []
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "GH_KEYS.json")
        with open(file_path, "r") as keys_file:
            keys_file = json.load(keys_file)
            keys_list: list = keys_file["keys"]
        return keys_list

    def get_github_connector(self, token_list: list) -> str:
        token: str = random.choice(token_list)
        github_connector = self.test_token(token=token)
        while not github_connector:
            token: str = random.choice(token_list)
            github_connector = self.test_token(token=token)

        return github_connector


class GHTokenUser(GHToken):
    def __init__(self) -> None:
        token_list = self.get_public_tokens(token=None)
        self.connector: Github = self.get_github_connector(token_list)


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


class GHCommit:
    def get_commits(self):
        commits = self.repo.get_commits()
        return commits

    def get_commit_data(self, commit: Commit.Commit):
        data = {
            "sha": commit.sha,
            "author_id": commit.author.id,
            "commiter_id": commit.committer.id,
            "project_id": self.repo.id,
            "created_at": format_dt(commit.commit.author.date),
        }
        print(f"commit data {data}")
        return data

    def get_commit_parents(self, commit: Commit.Commit):
        parents = commit.parents
        return parents

    def get_commit_comments(self, commit: Commit.Commit):
        comments = commit.get_comments()
        return comments

    def get_commit_comment_data(self, comment):
        data = {
            "id": comment.id,
            "user_id": comment.user.id,
            "commit_id": comment.commit_id,
            "created_at": format_dt(comment.created_at),
            "updated_at": format_dt(comment.updated_at),
            "body": comment.body,
        }
        print(f"comment data {data}")
        return data


class GHPullRequest:
    def get_pull_request_by_id(self, pull_id) -> PullRequest.PullRequest:
        pr = self.repo.get_pull(pull_id)
        return pr

    def get_repo_pull_requests(self) -> list:
        pulls = self.repo.get_pulls(state="all", sort="created", direction="desc")
        for pull in pulls:
            print(pull)
            break


class GHUser:
    def get_user_data(self, user: NamedUser.NamedUser):
        data = {
            "login": user.login,
            "name": user.name,
            "company": user.company,
            "location": user.location,
            "created_at": format_dt(user.created_at),
            "type": get_user_type(user.type),
        }
        print(f"User data {data}")

    def get_watcher_data(self, watcher: NamedUser.NamedUser):
        data = {"id": watcher.id, "created_at": watcher.created_at}
        print(f"watcher data {data}")
        return data

    def get_member_data(self, member: NamedUser.NamedUser):
        data = {
            "id": member.id,
            "created_at": member.created_at,
            "repo_id": self.repo.id,
        }
        print(f"member data {data}")
        return data


class GHLabel:
    def get_labels(self, entity: Union[Issue.Issue, Project.Project]):
        labels = entity.get_labels()
        return labels

    def get_label_data(self, label: Label.Label):
        data = {
            "repo_id": self.repo.id,
            "name": label.name,
        }
        print(f"label data {data}")
        return data


class GHExtractor(GHIssue, GHCommit, GHPullRequest, GHUser, GHLabel):
    def __init__(self, gh_user: GHTokenUser, gh_repo: str) -> None:
        self.connector: Github = gh_user.connector
        self.repo: Repository.Repository = self.connector.get_repo(gh_repo)

    def get_project_owner(self):
        owner = self.repo.owner
        return owner

    def get_watchers(self):
        watchers = self.repo.get_watchers()
        return watchers

    def get_members(self):
        members = self.repo.get_collaborators()
        return members
