from ..config import GHToken
from extract_service.repoinsights.repository import InsightsRepository
from extract_service.repoinsights.handlers.commit_handler import InsightsCommitHandler
from extract_service.repoinsights.handlers.project_user_handler import (
    InsightsProjectUserHandler,
)
from extract_service.repoinsights.handlers.label_handler import InsightsLabelHandler
from extract_service.repoinsights.handlers.issue_handler import InsightsIssueHandler
from extract_service.repoinsights.handlers.pull_request_handler import (
    InsightsPullRequestHandler,
)
from extract_service.repoinsights.handlers.repository_handler import (
    InsightsRepositoryHandler,
)
from extract_service.github_api.extractor import GitHubExtractor

from datetime import datetime
from loguru import logger
from typing import Union, List
from extract_service.utils.paralell import run_in_parallel


class ExtractDataClient:
    def __init__(
        self,
        owner: str,
        repo: str,
        since: Union[datetime, None],
        until: Union[datetime, None],
        data_types: List[str],
    ) -> None:
        self.data_types = data_types
        self.since = since
        self.until = until

        tokens = GHToken().get_public_tokens()
        tokens_iter = iter(tokens)

        self.repo = GitHubExtractor(owner, repo, tokens_iter)
        if self.repo.repositorio is None:
            raise Exception("Repository not found")

        self.commit_handler = InsightsCommitHandler(self.repo)
        self.project_handler = InsightsProjectUserHandler(self.repo)
        self.pull_request_handler = InsightsPullRequestHandler(self.repo)
        self.label_handler = InsightsLabelHandler(self.repo)
        self.issue_handler = InsightsIssueHandler(self.repo)
        self.repo_handler = InsightsRepositoryHandler(self.repo)

    def extract(self):
        args_list = [(data_type,) for data_type in self.data_types]
        args_list.append(("project",))
        results = run_in_parallel(self.extract_data, args_list)
        return results

    def extract_data(
        self,
        data_type: str,
    ):
        if data_type == "commits":
            commits = self.commit_handler.get_commits(self.since, self.until)
            extended_commits = list(commits)
            logger.info(f"Total GHCommits: {len(commits)}")
            return {"name": "commit", "data": extended_commits}
            for commit in commits:
                comments = client.commit_handler.get_commit_comments(commit.sha)
                print(f"Total comments: {len(comments)}")
                parents = client.commit_handler.get_commit_parents(commit.sha)
                print(f"Total parents: {len(parents)}")

        elif data_type == "project":
            projects = self.repo_handler.get_repo_info()
            logger.info("Project owner: {owner}", owner=projects["owner"]["login"])
            return {"name": "project", "data": projects}

        elif data_type == "pull_requests":
            prs = self.pull_request_handler.get_all_pull_requests(
                self.since, self.until
            )
            logger.info(f"Total GHPullRequests: {len(prs)}")
            return {"name": "pull_request", "data": prs}
            for pr in prs:
                pr_comments = client.pull_request_handler.get_pull_request_comments(pr)
                print(f"Total PR comments: {len(pr_comments)}")

        elif data_type == "issues":
            issues = self.issue_handler.get_issues(
                start_date=self.since, end_date=self.until
            )
            logger.info(f"Total GHIssues: {len(issues)}")
            return {"name": "issue", "data": issues}

            for issue in issues:
                events = client.issue_handler.get_issue_events(issue)
                print(f"Total events: {len(events)}")

        elif data_type == "labels":
            labels = self.label_handler.get_labels()
            logger.info(f"Total GHLabels: {len(labels)}")
            return {"name": "label", "data": labels}

        elif data_type == "members":
            members = self.project_handler.get_members(
                since=self.since, until=self.until
            )
            logger.info(f"Total members GHUser: {len(members)}")
            return {"name": "member", "data": members}

        elif data_type == "stargazers":
            stargazers = self.project_handler.get_stargazers(
                since=self.since, until=self.until
            )
            logger.info(f"Total stargazers GHUser: {len(stargazers)}")
            return {"name": "watchers", "data": stargazers}

        # elif data_type == "milestones":
        #     milestones = self.client.issue_handler.get_milestones()
        #     logger.info(f"Total GHMilestone: {len(milestones)}")
        #     return {"name": "milestone", "data": milestones}

        else:
            print(f"Invalid data type: {data_type}")
