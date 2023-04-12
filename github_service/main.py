from utils.paralell import run_in_parallel
from github_api.client import GitHubClient
from github_api.commit import GHCommit
from datetime import datetime
from utils.utils import is_valid_date
from pprint import pprint


def main():
    owner = "gousiosg"
    repo = "github-mirror"
    # since = datetime(2010, 1, 1)
    # until = datetime(2023, 1, 1)
    since = None
    until = None

    client = GitHubClient(owner, repo)

    data_types = [
        "commits",
        "pull_requests",
        "issues",
        "labels",
        "members",
        "watchers",
        "stargazers",
        "owner",
        "milestones",
    ]
    args_list = [(client, data_type, since, until) for data_type in data_types]
    results = run_in_parallel(extract_data, args_list)


def extract_data(
    client: GitHubClient, data_type: str, since: datetime, until: datetime
):
    if data_type == "commits":
        commits = client.commit_handler.get_commits(since, until)
        print(f"Total commits: {len(commits)}")
        # for commit in commits:
        #     comments = client.commit_handler.get_commit_comments(commit.sha)
        #     print(f"Total comments: {len(comments)}")
        #     parents = client.commit_handler.get_commit_parents(commit.sha)
        #     print(f"Total parents: {len(parents)}")

    elif data_type == "pull_requests":
        prs = client.pull_request_handler.get_all_pull_requests(since, until)
        print(f"Total pull requests: {len(prs)}")
        for pr in prs:
            pr_comments = client.pull_request_handler.get_pull_request_comments(pr)
            print(f"Total PR comments: {len(pr_comments)}")

    elif data_type == "issues":
        issues = client.issue_handler.get_issues(start_date=since, end_date=until)
        print(f"Total issues: {len(issues)}")
        for issue in issues:
            events = client.issue_handler.get_issue_events(issue)
            print(f"Total events: {len(events)}")

    elif data_type == "labels":
        labels = client.label_handler.get_labels()
        print(f"Total labels: {len(labels)}")

    elif data_type == "members":
        members = client.project_handler.get_members(since=since, until=until)
        print(f"Total members: {len(members)}")

    elif data_type == "watchers":
        watchers = client.project_handler.get_watchers(since=since, until=until)
        print(f"Total watchers: {len(watchers)}")

    elif data_type == "stargazers":
        stargazers = client.project_handler.get_stargazers(since=since, until=until)
        print(f"Total stargazers: {len(stargazers)}")

    elif data_type == "owner":
        owner = client.project_handler.get_owner()
        print(f"Owner: {owner.login}")

    elif data_type == "milestones":
        milestones = client.issue_handler.get_milestones()
        print(f"Total milestones: {len(milestones)}")

    else:
        print(f"Invalid data type: {data_type}")


if __name__ == "__main__":
    main()
