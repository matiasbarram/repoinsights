import requests

from services.extract_service.config import GHToken


tokens = GHToken().get_public_tokens()
TOKEN = tokens[0]
# Repository to analyze
REPO = "vitejs/vite"

headers = {"Authorization": f"Token {TOKEN}"}


def get_data(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}")
    return response.json(), response.headers


def get_number_of_pages(url):
    data, response_headers = get_data(url)
    if "link" in response_headers:
        pages = {
            rel[6:-1]: url[url.index("<") + 1 : -1]
            for url, rel in (
                link.split(";") for link in response_headers["link"].split(",")
            )
        }
        return int(pages["last"].split("=")[-1])
    else:
        return 1


# Get number of commits
commit_url = f"https://api.github.com/repos/{REPO}/commits?per_page=1&page=1"
commit_pages = get_number_of_pages(commit_url)

# Get number of commit comments
commit_comments_url = f"https://api.github.com/repos/{REPO}/comments?per_page=1&page=1"
commit_comments_pages = get_number_of_pages(commit_comments_url)

# Get number of pull requests
pr_url = f"https://api.github.com/repos/{REPO}/pulls?per_page=1&page=1"
pr_pages = get_number_of_pages(pr_url)

# Get number of pull request comments
pr_comments_url = (
    f"https://api.github.com/repos/{REPO}/pulls/comments?per_page=1&page=1"
)
pr_comments_pages = get_number_of_pages(pr_comments_url)

# For each PR, you have to call at least 1 and at most 3 commit pages
# I use the average of 2 here
pr_commit_pages = 2 * pr_pages

# Get number of issues
issues_url = f"https://api.github.com/repos/{REPO}/issues?per_page=1&page=1"
issues_pages = get_number_of_pages(issues_url)

# Get number of issue comments
issue_comments_url = (
    f"https://api.github.com/repos/{REPO}/issues/comments?per_page=1&page=1"
)
issue_comments_pages = get_number_of_pages(issue_comments_url)

# Get number of labels
labels_url = f"https://api.github.com/repos/{REPO}/labels?per_page=1&page=1"
labels_pages = get_number_of_pages(labels_url)

# Get number of milestones
milestones_url = f"https://api.github.com/repos/{REPO}/milestones?per_page=1&page=1"
milestones_pages = get_number_of_pages(milestones_url)

# Calculate total
total = (
    2
    + 3 * commit_pages
    + 2 * commit_comments_pages
    + 9 * pr_pages
    + 2 * pr_comments_pages
    + pr_commit_pages
    + 3 * issues_pages
    + issue_comments_pages
    + labels_pages
    + milestones_pages
)

print(f"Total API calls: {total}")
