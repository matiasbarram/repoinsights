from github_service.utils.paralell import run_in_parallel
from github_service.github_api.client import GitHubClient
from github_service.github_api.commit import GHCommit
from datetime import datetime
from github_service.utils.utils import is_valid_date
from pprint import pprint
import json
from db_connector.connector import DBConnector
from test_load import LoadData
from loguru import logger


class ExtractData:
    def __init__(self, client: GitHubClient, owner, repo, since, until, data_types):
        self.client = client
        self.owner = owner
        self.repo = repo
        self.since = since
        self.until = until
        self.data_types = data_types

    def load(self):
        args_list = [
            (self.client, data_type, self.since, self.until)
            for data_type in self.data_types
        ]
        results = run_in_parallel(self.extract_data, args_list)
        LoadData(self.client).load_data(results)

    def extract_data(
        self, client: GitHubClient, data_type: str, since: datetime, until: datetime
    ):
        if data_type == "commits":
            commits = self.client.commit_handler.get_commits(self.since, self.until)
            extended_commits = list(commits)
            logger.info(f"Total GHCommits: {len(commits)}")
            return {"name": "commit", "data": extended_commits}
            for commit in commits:
                comments = client.commit_handler.get_commit_comments(commit.sha)
                print(f"Total comments: {len(comments)}")
                parents = client.commit_handler.get_commit_parents(commit.sha)
                print(f"Total parents: {len(parents)}")

        elif data_type == "pull_requests":
            prs = self.client.pull_request_handler.get_all_pull_requests(
                self.since, self.until
            )
            logger.info(f"Total GHPullRequests: {len(prs)}")
            return {"name": "pull_request", "data": prs}
            for pr in prs:
                pr_comments = client.pull_request_handler.get_pull_request_comments(pr)
                print(f"Total PR comments: {len(pr_comments)}")

        elif data_type == "issues":
            issues = self.client.issue_handler.get_issues(
                start_date=self.since, end_date=self.until
            )
            logger.info(f"Total GHIssues: {len(issues)}")
            return {"name": "issue", "data": issues}
            for issue in issues:
                events = client.issue_handler.get_issue_events(issue)
                print(f"Total events: {len(events)}")

        elif data_type == "labels":
            labels = self.client.label_handler.get_labels()
            logger.info(f"Total GHLabels: {len(labels)}")
            return {"name": "label", "data": labels}

        elif data_type == "members":
            members = self.client.project_handler.get_members(
                since=self.since, until=self.until
            )
            logger.info(f"Total members GHUser: {len(members)}")
            return {"name": "member", "data": members}

        elif data_type == "watchers":
            watchers = self.client.project_handler.get_watchers(
                since=self.since, until=self.until
            )
            logger.info(f"Total watchers GHWatchers: {len(watchers)}")
            return {"name": "watcher", "data": watchers}

        elif data_type == "stargazers":
            stargazers = self.client.project_handler.get_stargazers(
                since=self.since, until=self.until
            )
            logger.info(f"Total stargazers GHUser: {len(stargazers)}")
            return {"name": "stargazer", "data": stargazers}

        elif data_type == "owner":
            owner = self.client.project_handler.get_owner()
            logger.info("Owner GHUser: {owner}", owner=owner.login)
            return {"name": "owner", "data": owner}

        elif data_type == "milestones":
            milestones = self.client.issue_handler.get_milestones()
            logger.info(f"Total GHMilestone: {len(milestones)}")
            return {"name": "milestone", "data": milestones}

        else:
            print(f"Invalid data type: {data_type}")


def main():
    owner = "RepoReapers"
    repo = "reaper"
    since = datetime(2015, 1, 10)
    until = datetime(2019, 12, 20)
    # since = None
    # until = None

    client = GitHubClient(owner, repo)
    data_types = [
        "owner",
        "commits",
        "pull_requests",  # revisar
        "issues",
        # "labels",
        # "stargazers",  # eliminar, es lo mismo que watchers.
        # "watchers",  # se demora mucho, siempre se deben traer todos
        # "members",  # se demora mucho, siempre se deben traer todos
        # "milestones",
    ]

    extract_data = ExtractData(
        client=client,
        owner=owner,
        repo=repo,
        since=since,
        until=until,
        data_types=data_types,
    )

    extract_data.load()


if __name__ == "__main__":
    logger.add("logs/extract_data_{time}.log")
    main()
