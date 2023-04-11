from github import Commit
from helper.utils import format_dt
from .GHRepository import GHRepository
from datetime import datetime


class GHCommit(GHRepository):
    def get_commits(self):
        commits = self.repo.get_commits()
        return commits

    def get_commits_between_dates(self, since=datetime, until=datetime):
        commits = self.repo.get_commits(since=since, until=until)
        return commits

    def get_commit_data(self, commit: Commit.Commit):
        author_id = commit.author.id if commit.author is not None else None
        commiter_id = commit.committer.id if commit.committer is not None else None

        data = {
            "sha": commit.sha,
            "author_id": author_id,
            "commiter_id": commiter_id,
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
