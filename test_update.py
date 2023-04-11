from GithubExtractor.GHCommit import GHCommit
from GithubExtractor.GHGetToken import GHGetToken
from DWConnector.repositories.project_repositories import ProjectRepository
from pprint import pprint
from datetime import datetime

TEST_DATE = datetime(2013, 12, 1)
PROJECT_DATA = {
    "id": 1,
    "name": "akka/akka",
}


class ExtractService:
    def db_get_last_commit(self, project_id):
        project_repo = ProjectRepository()
        last_commit = project_repo.get_last_commit(project_id)
        if last_commit is None:
            exit()
        commit, project, user = last_commit
        return {
            "date": commit.created_at,
            "commiter": user.login,
            "project": project.name,
        }

    def get_commits_data(self, commits, gh_commit):
        total_commits = []
        for commit in commits:
            commit_data = gh_commit.get_commit_data(commit)
            pprint(commit_data)
            total_commits.append(commit_data)
        return total_commits

    def gh_get_new_commits(self, project_name: str, last_commit_data: dict):
        gh_token = GHGetToken()
        gh_commit = GHCommit(gh_token, project_name)
        since: datetime = last_commit_data["date"]
        commits = gh_commit.get_commits_between_dates(since=since, until=TEST_DATE)
        commits_data = self.get_commits_data(commits, gh_commit)
        print(f"commits count {len(list(commits))}")
        return commits_data

    # Add data in temporal database
    def db_update_last_commit(self, data: dict):
        # connect to temporal database
        # insert data
        pass


extract_service = ExtractService()
last_commit_data = extract_service.db_get_last_commit(PROJECT_DATA["id"])
commits = extract_service.gh_get_new_commits(PROJECT_DATA["name"], last_commit_data)
extract_service.db_update_last_commit(commits)
