from utils.paralell import run_in_parallel
from github_api.client import GitHubClient
from github_api.commit import GHCommit
from datetime import datetime
from utils.utils import is_valid_date
from pprint import pprint


def main():
    owner = "gousiosg"
    repo = "github-mirror"
    since = datetime(2015, 1, 1)
    until = datetime(2016, 1, 1)

    client = GitHubClient(owner, repo)

    data_types = ["commits", "pull_requests", "issues", "labels", "users"]
    args_list = [(client, data_type, since, until) for data_type in data_types]
    results = run_in_parallel(extract_data, args_list)
    print(results)


def extract_data(
    client: GitHubClient, data_type: str, since: datetime, until: datetime
):
    if data_type == "commits":
        commits = client.commit_handler.get_commits_between_dates(since, until)
        print(f"Total commits: {len(commits)}")

    elif data_type == "pull_requests":
        prs = client.pull_request_handler.get_pull_requests_between_dates(since, until)
        print(f"Total pull requests: {len(prs)}")

    elif data_type == "issues":
        issues = client.issue_handler.get_issues_between_dates(since, until)
        print(f"Total issues: {len(issues)}")

    elif data_type == "labels":
        labels = client.label_handler.get_labels()
        print(f"Total labels: {len(labels)}")

    # elif data_type == "users":
    #     members = client.project_handler.get_members()
    #     watchers = client.project_handler.get_watchers()
    #     owner = client.project_handler.get_owner()
    #     print({"members": len(members), "watchers": len(watchers), "owner": owner})

    else:
        print(f"Invalid data type: {data_type}")


if __name__ == "__main__":
    main()
