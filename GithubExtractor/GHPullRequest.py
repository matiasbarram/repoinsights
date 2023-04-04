from github import PullRequest, PullRequestComment, PaginatedList
from .GHRepository import GHRepository


class GHPullRequest(GHRepository):
    def get_pull_request_by_id(self, pull_id):
        pr = self.repo.get_pull(pull_id)
        return pr

    def get_pulls(self):
        return self.repo.get_pulls(state="all", sort="created", direction="desc")

    def get_pull_data(self, pull: PullRequest.PullRequest):
        data = {
            "id": pull.id,
            "repo_id": self.repo.id,
            "number": pull.number,
            "title": pull.title,
            "body": pull.body,
            "state": pull.state,
            # "locked": pull.locked,
            "created_at": pull.created_at,
            "updated_at": pull.updated_at,
            "closed_at": pull.closed_at,
            "merged_at": pull.merged_at,
            "merge_commit_sha": pull.merge_commit_sha,
            "mergeable": pull.mergeable,
            "merged": pull.merged,
            "rebaseable": pull.rebaseable,
            "mergeable_state": pull.mergeable_state,
            "merged_by_id": pull.merged_by.id if pull.merged_by else None,
            "comments": pull.comments,
            "review_comments": pull.review_comments,
            "commits": pull.commits,
            "additions": pull.additions,
            "deletions": pull.deletions,
            "changed_files": pull.changed_files,
        }
        print(f"Pull request data {data}")
        return data

    def get_pull_comments(self, pull: PullRequest.PullRequest):
        comments = pull.get_comments()
        return comments

    def get_pull_comment_data(
        self,
        pull: PullRequest.PullRequest,
        comment: PullRequestComment.PullRequestComment,
    ):
        data = {
            "id": comment.id,
            "user_id": comment.user.id,  # GET ID FROM DB
            "pull_request_id": pull.id,  # GET ID FROM DB
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
            "body": comment.body,
        }
        print(f"comment data {data}")
        return data
