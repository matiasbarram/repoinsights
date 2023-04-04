from github import PullRequest


class GHPullRequest:
    def get_pull_request_by_id(self, pull_id) -> PullRequest.PullRequest:
        pr = self.repo.get_pull(pull_id)
        return pr

    def get_repo_pull_requests(self) -> list:
        pulls = self.repo.get_pulls(state="all", sort="created", direction="desc")
        for pull in pulls:
            print(pull)
            break
