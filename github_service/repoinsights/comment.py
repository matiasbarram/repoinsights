from github.CommitComment import CommitComment
from github.IssueComment import IssueComment
from github.PullRequestComment import PullRequestComment


class GHComment:
    def __init__(self, id, body, author, created_at, updated_at):
        self.id = id
        self.body = body
        self.author = author
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "body": self.body,
            "author": self.author,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class GHPullRequestComment(GHComment):
    def __init__(self, comment: PullRequestComment):
        super().__init__(
            id=comment.id,
            body=comment.body,
            author=comment.user.login if comment.user else None,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )


class GHIssueComment(GHComment):
    def __init__(self, comment: IssueComment):
        super().__init__(
            id=comment.id,
            body=comment.body,
            author=comment.user.login if comment.user else None,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )


class GHCommitComment(GHComment):
    def __init__(self, comment: CommitComment):
        super().__init__(
            id=comment.id,
            body=comment.body,
            author=comment.user.login if comment.user else None,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
