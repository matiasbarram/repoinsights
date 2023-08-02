import requests
import math
from services.extract_service.config import GHToken

# Set API token and headers
token = GHToken().get_token_lowest_wait_time(only_token=True)
headers = {"Authorization": f"Token {token}"}

# repository to analyze
repo = "FortAwesome/Font-Awesome"


# Function to get total number of items and calculate pages
def get_total_items_and_calculate_pages(url):
    response = requests.get(url, headers=headers, params={"per_page": 1, "page": 1})
    if response.status_code != 200:
        print(response.json())
        raise Exception(f"Request failed with status {response.status_code}")

    if "Link" in response.headers:
        link_header = response.headers["Link"]
        links = link_header.split(", ")
        last_link = [link for link in links if 'rel="last"' in link][0]
        last_page = last_link.split("&page=")[1].split(">")[0]
        total_items = int(last_page)
    else:
        items = response.json()
        total_items = len(items)
    if total_items == 0:
        total_pages = 1
    else:
        total_pages = math.ceil(total_items / 100)
    print(f"{url} Total items: {total_items}, total pages: {total_pages}")
    return total_items, total_pages


def calculate(repo) -> int:
    endpoints = {
        "commits": f"https://api.github.com/repos/{repo}/commits",
        "commit_comments": f"https://api.github.com/repos/{repo}/comments",
        "pull_requests": f"https://api.github.com/repos/{repo}/pulls?state=all",
        "pull_request_comments": f"https://api.github.com/repos/{repo}/pulls/comments",
        "issues": f"https://api.github.com/repos/{repo}/issues",
        "issue_comments": f"https://api.github.com/repos/{repo}/issues/comments",
        "labels": f"https://api.github.com/repos/{repo}/labels",
        "milestones": f"https://api.github.com/repos/{repo}/milestones",
    }
    total_calls = 0
    total_issues = 0
    total_prs = 0
    for name, url in endpoints.items():
        total_items, total_pages = get_total_items_and_calculate_pages(url)
        if name == "issues":
            total_issues = total_items
        if name == "pull_requests":
            total_prs = total_items

        if name == "pull_requests":
            total_calls += total_pages + (6 * total_items)
        elif name == "commits":
            total_calls += total_pages + (2 * total_items)
        elif name == "issues":
            total_calls += total_pages + (4 * total_items)
        elif name == "issue_comments":
            total_calls += total_pages + (2 * total_issues)
        elif name == "commit_comments":
            total_calls += total_pages + total_items
        elif name in ["pull_request_comments"]:
            total_calls += total_pages + total_prs
        else:
            total_calls += total_pages

    total_calls += 2
    return total_calls


if __name__ == "__main__":
    print(calculate(repo))
