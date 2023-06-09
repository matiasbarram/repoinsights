from services.traspaso_service.traspaso.get_from_temp import TempClient
from services.traspaso_service.db_connector.database_handler import DatabaseHandler
from services.traspaso_service.add_to_consolidada import ConsolidatedClient
from loguru import logger


class Client:
    def __init__(self, db: DatabaseHandler, uuid: str) -> None:
        self.db = db
        self.uuid = uuid

    def migrate(self):
        """
        Obtener los datos de temportal con el uuid del proyecto
        """
        temp = TempClient(self.db, self.uuid)
        users = temp.get_users()
        projects = temp.get_projects()
        extractions = temp.get_extractions()
        project_members = temp.get_project_members()
        labels = temp.get_labels()
        milestones = temp.get_milestones()

        commits = temp.get_commits()
        commit_comments = temp.get_commit_comments()
        commit_parents = temp.get_commit_parents()
        issues = temp.get_issues()
        issue_comments = temp.get_issue_comments()
        issue_events = temp.get_issue_events()
        issue_labels = temp.get_issue_labels()
        prs = temp.get_prs()
        pr_comments = temp.get_pr_comments()
        pr_history = temp.get_pr_history()
        pr_commits = temp.get_pr_commits()
        watchers = temp.get_watchers()
        followers = temp.get_followers()

        logger.info("Migrando data... {uuid}", uuid=self.uuid)
        print(f"Users: {len(users)}")

        print(f"Watchers: {len(watchers)}")
        print(f"Followers: {len(followers)}")
        print(f"Projects: {len(projects)}")
        print(f"Labels: {len(labels)}")
        print(f"Milestones: {len(milestones)}")

        print(f"Commits: {len(commits)}")
        print(f"Commit Comments: {len(commit_comments)}")
        print(f"Commit Parents: {len(commit_parents)}")

        print(f"Issues: {len(issues)}")
        print(f"Issue Comments: {len(issue_comments)}")
        print(f"Issue Events: {len(issue_events)}")
        print(f"Issue Labels: {len(issue_labels)}")

        print(f"Pull Requests: {len(prs)}")
        print(f"Pull Request Comments: {len(pr_comments)}")
        print(f"Pull Request History: {len(pr_history)}")
        print(f"Pull Request Commits: {len(pr_commits)}")

        # if all are 0
        if (
            len(users) == 0
            and len(projects) == 0
            and len(extractions) == 0
            and len(project_members) == 0
            and len(labels) == 0
            and len(milestones) == 0
            and len(commits) == 0
            and len(commit_comments) == 0
            and len(commit_parents) == 0
            and len(issues) == 0
            and len(issue_comments) == 0
            and len(issue_events) == 0
            and len(issue_labels) == 0
            and len(prs) == 0
            and len(pr_comments) == 0
            and len(pr_history) == 0
            and len(watchers) == 0
            and len(followers) == 0
        ):
            logger.error("No data to traspasar")
            exit(0)

        consolidada = ConsolidatedClient(self.uuid, self.db)
        consolidada.add_users(users)

        consolidada.add_projects(projects)
        consolidada.add_extractions(extractions)
        consolidada.add_project_members(project_members)

        consolidada.add_labels(labels)
        consolidada.add_milestones(milestones)

        consolidada.add_watchers(watchers)
        consolidada.add_followers(followers)

        consolidada.add_commits(commits)
        consolidada.add_commit_comments(commit_comments)
        consolidada.add_commit_parents(commit_parents)

        consolidada.add_pull_requests(prs)
        consolidada.add_pull_request_comments(pr_comments)
        consolidada.add_pull_request_history(pr_history)
        consolidada.add_pull_request_commits(pr_commits)

        consolidada.add_issues(issues)
        consolidada.add_issue_comments(issue_comments)
        consolidada.add_issue_events(issue_events)
        consolidada.add_issue_labels(issue_labels)

        # DELETE FROM TEMPORAL IN REVERSE ORDER USING ext_ref_id
        # temp.delete_issue_labels()
        # temp.delete_issue_events()
        # temp.delete_issue_comments()
        # temp.delete_issues()
        # temp.delete_pr_commits()
        # temp.delete_pr_history()
        # temp.delete_pr_comments()
        # temp.delete_prs()
        # temp.delete_commit_parents()
        # temp.delete_commit_comments()
        # temp.delete_commits()
        # temp.delete_milestones()
        # temp.delete_labels()
        # temp.delete_project_members()
        # temp.delete_extractions()
        # temp.delete_projects()
        # temp.delete_followers()
        # temp.delete_watchers()
        # temp.delete_users()
        # logger.info("Data migrada {uuid}", uuid=self.uuid)
