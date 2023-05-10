import datetime
from services.traspaso_service.get_from_temp import TempClient
from services.traspaso_service.utils.utils import get_from_map
from services.traspaso_service.db_connector.models import (
    User,
    Project,
    Commit,
    CommitComment,
    CommitParent,
    Follower,
    Fork,
    Issue,
    IssueComment,
    IssueEvent,
    IssueLabel,
    OrganizationMember,
    ProjectCommit,
    ProjectMember,
    PullRequest,
    PullRequestComment,
    PullRequestCommit,
    PullRequestHistory,
    RepoLabel,
    RepoMilestone,
    Watcher,
)
from services.traspaso_service.db_connector.database_handler import DatabaseHandler
import pandas as pd
from sqlalchemy.orm import Session
from pprint import pprint
from loguru import logger
from typing import List, Dict, Any, Tuple, Union


class Client:
    def __init__(self, db: DatabaseHandler, uuid: str) -> None:
        self.db = db
        self.uuid = uuid
        self.temp = TempClient(self.db, self.uuid)

        self.user_id_map = {}
        self.project_id_map = {}
        self.commit_id_map = {}
        self.commit_comment_id_map = {}
        self.issue_id_map = {}
        self.pull_request_id_map = {}
        self.pull_request_history_id_map = {}
        self.label_id_map = {}

    def add_users(self, users: List[User]):
        for user in users:
            # Verifica si el usuario ya existe en la base de datos consolidada
            existing_user = (
                self.db.session_consolidada.query(User)
                .filter_by(login=user.login)
                .first()
            )

            if existing_user is None:
                old_id = user.id
                new_user = User(
                    login=user.login,
                    name=user.name,
                    email=user.email,
                    company=user.company,
                    location=user.location,
                    created_at=user.created_at,
                    ext_ref_id=self.uuid,
                    type=user.type,
                )

                self.db.session_consolidada.add(new_user)
                self.db.session_consolidada.commit()
                self.user_id_map[old_id] = new_user.id
            else:
                self.user_id_map[user.id] = existing_user.id

    def add_main_project(self, projects: List[Project]):
        consolidada_main_project = None
        temp_main_project = None

        for project in projects:
            if project.forked_from is None:
                temp_main_project = project
                break
        if temp_main_project is None:
            # obtener project from consolidada usando info de la cola
            # este caso ocurre cuando el proyecto principal no se extrajo pero si esta en consolidada
            raise Exception("No se encontró un proyecto no forkeado")

        project = temp_main_project
        exist_in_consolidada = (
            self.db.session_consolidada.query(Project)
            .filter_by(
                owner_id=get_from_map(self.user_id_map, project.owner_id),
                name=project.name,
            )
            .first()
        )
        if exist_in_consolidada is not None:
            self.project_id_map[project.id] = exist_in_consolidada.id
            return exist_in_consolidada.id

        consolidada_main_project = Project(
            url=project.url,
            owner_id=get_from_map(self.user_id_map, project.owner_id),
            name=project.name,
            description=project.description,
            language=project.language,
            created_at=project.created_at,
            ext_ref_id=self.uuid,
            forked_from=project.forked_from,
            deleted=project.deleted,
            last_extraction=project.last_extraction,
        )
        self.db.session_consolidada.add(consolidada_main_project)
        self.db.session_consolidada.commit()
        self.project_id_map[project.id] = consolidada_main_project.id

        if consolidada_main_project is None:
            raise Exception("No se encontró un proyecto no forkeado")

        return consolidada_main_project.id

    def add_projects(self, projects: List[Project]):
        main_project_id = self.add_main_project(projects)
        for project in projects:
            if project.forked_from is None:
                continue
            owner_id = get_from_map(self.user_id_map, project.owner_id)
            existing_project = (
                self.db.session_consolidada.query(Project)
                .filter_by(owner_id=owner_id, name=project.name)
                .first()
            )
            if existing_project is None:
                old_id = project.id
                new_project = Project(
                    url=project.url,
                    owner_id=owner_id,
                    name=project.name,
                    description=project.description,
                    language=project.language,
                    created_at=project.created_at,
                    ext_ref_id=self.uuid,
                    forked_from=main_project_id,
                    deleted=project.deleted,
                    last_extraction=project.last_extraction,
                )
                self.db.session_consolidada.add(new_project)
                self.db.session_consolidada.commit()
                self.project_id_map[old_id] = new_project.id
            else:
                self.project_id_map[project.id] = existing_project.id

    def add_commits(self, commits: List[Commit]):
        for commit in commits:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            project_id = get_from_map(self.project_id_map, commit.project_id)

            # Verifica si el commit ya existe en la base de datos consolidada
            existing_commit = (
                self.db.session_consolidada.query(Commit)
                .filter_by(project_id=project_id, sha=commit.sha)
                .first()
            )

            if existing_commit is None:
                new_commit = Commit(
                    sha=commit.sha,
                    author_id=get_from_map(self.user_id_map, commit.author_id),
                    committer_id=get_from_map(self.user_id_map, commit.committer_id),
                    project_id=project_id,
                    created_at=commit.created_at,
                    message=commit.message,
                    ext_ref_id=self.uuid,
                )
                self.db.session_consolidada.add(new_commit)
                self.db.session_consolidada.commit()
                self.commit_id_map[commit.id] = new_commit.id
            else:
                self.commit_id_map[commit.id] = existing_commit.id

    def add_commit_comments(self, commit_comments: List[CommitComment]):
        for commit_comment in commit_comments:
            # Obtén el commit correspondiente en la base de datos consolidada
            commit_id = get_from_map(self.commit_id_map, commit_comment.commit_id)

            # Verifica si el commit ya existe en la base de datos consolidada
            existing_commit_comment = (
                self.db.session_consolidada.query(CommitComment)
                .filter_by(
                    commit_id=commit_id,
                    user_id=get_from_map(self.user_id_map, commit_comment.user_id),
                )
                .first()
            )

            if existing_commit_comment is None:
                new_commit_comment = CommitComment(
                    commit_id=commit_id,
                    user_id=get_from_map(self.user_id_map, commit_comment.user_id),
                    body=commit_comment.body,
                    line=commit_comment.line,
                    position=commit_comment.position,
                    comment_id=commit_comment.comment_id,
                    ext_ref_id=self.uuid,
                    created_at=commit_comment.created_at,
                )
                self.db.session_consolidada.add(new_commit_comment)
                self.db.session_consolidada.commit()
                self.commit_comment_id_map[commit_comment.id] = new_commit_comment.id

            else:
                self.commit_comment_id_map[
                    commit_comment.id
                ] = existing_commit_comment.id

    def add_pull_requests(self, pull_requests: List[PullRequest]):
        for pull_request in pull_requests:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            head_repo_id = get_from_map(self.project_id_map, pull_request.head_repo_id)
            base_repo_id = get_from_map(self.project_id_map, pull_request.base_repo_id)
            head_commit_id = get_from_map(
                self.commit_id_map, pull_request.head_commit_id
            )
            base_commit_id = get_from_map(
                self.commit_id_map, pull_request.base_commit_id
            )
            user_id = get_from_map(self.user_id_map, pull_request.user_id)

            # Verifica si el pull request ya existe en la base de datos consolidada
            existing_pull_request = (
                self.db.session_consolidada.query(PullRequest)
                .filter_by(
                    head_commit_id=head_commit_id,
                    base_commit_id=base_commit_id,
                    pullreq_id=pull_request.pullreq_id,
                )
                .first()
            )

            if existing_pull_request is None:
                new_pull_request = PullRequest(
                    head_repo_id=head_repo_id,
                    base_repo_id=base_repo_id,
                    head_commit_id=head_commit_id,
                    base_commit_id=base_commit_id,
                    user_id=user_id,
                    pullreq_id=pull_request.pullreq_id,
                    intra_branch=pull_request.intra_branch,
                    # additions=pull_request.additions,
                    # deletions=pull_request.deletions,
                    # changed_files=pull_request.changed_files,
                    merged=pull_request.merged,
                    ext_ref_id=self.uuid,
                )
                self.db.session_consolidada.add(new_pull_request)
                self.db.session_consolidada.commit()
                self.pull_request_id_map[pull_request.id] = new_pull_request.id
            else:
                self.pull_request_id_map[pull_request.id] = existing_pull_request.id

    def add_issues(self, issues: List[Issue]):
        for issue in issues:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            repo_id = get_from_map(self.project_id_map, issue.repo_id)
            reporter_id = get_from_map(self.user_id_map, issue.reporter_id)
            assignee_id = get_from_map(self.user_id_map, issue.assignee_id)
            pull_request_id = get_from_map(
                self.pull_request_id_map, issue.pull_request_id
            )

            # Verifica si el issue ya existe en la base de datos consolidada
            existing_issue = (
                self.db.session_consolidada.query(Issue)
                .filter_by(repo_id=repo_id, issue_id=issue.issue_id)
                .first()
            )

            if existing_issue is None:
                new_issue = Issue(
                    repo_id=repo_id,
                    reporter_id=reporter_id,
                    assignee_id=assignee_id,
                    issue_id=issue.issue_id,
                    pull_request=issue.pull_request,
                    pull_request_id=pull_request_id,
                    created_at=issue.created_at,
                    ext_ref_id=self.uuid,
                )
                self.db.session_consolidada.add(new_issue)
                self.db.session_consolidada.commit()
                self.issue_id_map[issue.id] = new_issue.id
            else:
                self.issue_id_map[issue.id] = existing_issue.id

    def add_pull_request_comments(
        self, pull_request_comments: List[PullRequestComment]
    ):
        for pull_request_comment in pull_request_comments:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            pull_request_id = get_from_map(
                self.pull_request_id_map, pull_request_comment.pull_request_id
            )

            user_id = get_from_map(self.user_id_map, pull_request_comment.user_id)
            commit_id = get_from_map(self.commit_id_map, pull_request_comment.commit_id)

            # Verifica si el pull request comment ya existe en la base de datos consolidada
            existing_pull_request_comment = (
                self.db.session_consolidada.query(PullRequestComment)
                .filter_by(
                    pull_request_id=pull_request_id,
                    user_id=user_id,
                    comment_id=pull_request_comment.comment_id,
                    commit_id=commit_id,
                )
                .first()
            )

            if existing_pull_request_comment is None:
                new_pull_request_comment = PullRequestComment(
                    pull_request_id=pull_request_id,
                    user_id=user_id,
                    comment_id=pull_request_comment.comment_id,
                    position=pull_request_comment.position,
                    body=pull_request_comment.body,
                    commit_id=commit_id,
                    created_at=pull_request_comment.created_at,
                    ext_ref_id=self.uuid,
                )

                self.db.session_consolidada.add(new_pull_request_comment)
                self.db.session_consolidada.commit()

    def add_pull_request_history(self, pull_request_history: List[PullRequestHistory]):
        for pull_request_history in pull_request_history:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            pull_request_id = get_from_map(
                self.pull_request_id_map, pull_request_history.pull_request_id
            )
            actor_id = get_from_map(self.user_id_map, pull_request_history.actor_id)

            # Verifica si el pull request comment ya existe en la base de datos consolidada
            existing_pull_request_history = (
                self.db.session_consolidada.query(PullRequestHistory)
                .filter_by(
                    pull_request_id=pull_request_id,
                    actor_id=actor_id,
                    created_at=pull_request_history.created_at,
                )
                .first()
            )

            if existing_pull_request_history is None:
                new_pull_request_history = PullRequestHistory(
                    pull_request_id=pull_request_id,
                    created_at=pull_request_history.created_at,
                    actor_id=actor_id,
                    ext_ref_id=self.uuid,
                    action=pull_request_history.action,
                )

                self.db.session_consolidada.add(new_pull_request_history)
                self.db.session_consolidada.commit()
                self.pull_request_history_id_map[
                    pull_request_history.id
                ] = new_pull_request_history.id
            else:
                self.pull_request_history_id_map[
                    pull_request_history.id
                ] = existing_pull_request_history.id

    def add_issue_comments(self, issue_comments: List[IssueComment]):
        for issue_comment in issue_comments:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            issue_id = get_from_map(self.issue_id_map, issue_comment.issue_id)
            user_id = get_from_map(self.user_id_map, issue_comment.user_id)

            # Verifica si el pull request comment ya existe en la base de datos consolidada
            existing_issue_comment = (
                self.db.session_consolidada.query(IssueComment)
                .filter_by(
                    issue_id=issue_id,
                    user_id=user_id,
                    comment_id=issue_comment.comment_id,
                )
                .first()
            )

            if existing_issue_comment is None:
                new_issue_comment = IssueComment(
                    issue_id=issue_id,
                    user_id=user_id,
                    comment_id=issue_comment.comment_id,
                    created_at=issue_comment.created_at,
                    ext_ref_id=self.uuid,
                )

                self.db.session_consolidada.add(new_issue_comment)
                self.db.session_consolidada.commit()

    def add_issue_events(self, issue_events: List[IssueEvent]):
        for issue_event in issue_events:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            issue_id = get_from_map(self.issue_id_map, issue_event.issue_id)
            actor_id = get_from_map(self.user_id_map, issue_event.actor_id)

            # Verifica si el pull request comment ya existe en la base de datos consolidada
            existing_issue_event = (
                self.db.session_consolidada.query(IssueEvent)
                .filter_by(
                    issue_id=issue_id,
                    actor_id=actor_id,
                    created_at=issue_event.created_at,
                )
                .first()
            )

            if existing_issue_event is None:
                new_issue_event = IssueEvent(
                    event_id=issue_event.event_id,
                    issue_id=issue_id,
                    actor_id=actor_id,
                    action=issue_event.action,
                    action_specific=issue_event.action_specific,
                    created_at=issue_event.created_at,
                    ext_ref_id=self.uuid,
                )

                self.db.session_consolidada.add(new_issue_event)
                self.db.session_consolidada.commit()

    def add_labels(self, labels: List[RepoLabel]):
        for label in labels:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            repo_id = get_from_map(self.project_id_map, label.repo_id)

            # Verifica si el pull request comment ya existe en la base de datos consolidada
            existing_label = (
                self.db.session_consolidada.query(RepoLabel)
                .filter_by(
                    repo_id=repo_id,
                    name=label.name,
                )
                .first()
            )

            if existing_label is None:
                new_label = RepoLabel(
                    repo_id=repo_id,
                    name=label.name,
                    ext_ref_id=self.uuid,
                )

                self.db.session_consolidada.add(new_label)
                self.db.session_consolidada.commit()
                self.label_id_map[label.id] = new_label.id
            else:
                self.label_id_map[label.id] = existing_label.id

    def add_issue_labels(self, issue_labels: List[IssueLabel]):
        for issue_label in issue_labels:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            label_id = get_from_map(self.label_id_map, issue_label.label_id)
            issue_id = get_from_map(self.issue_id_map, issue_label.issue_id)

            # Verifica si el pull request comment ya existe en la base de datos consolidada
            existing_issue_label = (
                self.db.session_consolidada.query(IssueLabel)
                .filter_by(
                    issue_id=issue_id,
                    label_id=label_id,
                )
                .first()
            )

            if existing_issue_label is None:
                new_issue_label = IssueLabel(
                    issue_id=issue_id,
                    label_id=label_id,
                    ext_ref_id=self.uuid,
                )

                self.db.session_consolidada.add(new_issue_label)
                self.db.session_consolidada.commit()

    def add_milestones(self, milestones: List[RepoMilestone]):
        for milestone in milestones:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            repo_id = get_from_map(self.project_id_map, milestone.repo_id)

            # Verifica si el pull request comment ya existe en la base de datos consolidada
            existing_milestone = (
                self.db.session_consolidada.query(RepoMilestone)
                .filter_by(
                    repo_id=repo_id,
                    name=milestone.name,
                )
                .first()
            )

            if existing_milestone is None:
                new_milestone = RepoMilestone(
                    repo_id=repo_id,
                    name=milestone.name,
                    ext_ref_id=self.uuid,
                )
                self.db.session_consolidada.add(new_milestone)
                self.db.session_consolidada.commit()

    def add_watchers(self, watchers: List[Watcher]):
        for watcher in watchers:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            repo_id = get_from_map(self.project_id_map, watcher.repo_id)
            user_id = get_from_map(self.user_id_map, watcher.user_id)

            # Verifica si el pull request comment ya existe en la base de datos consolidada
            existing_watcher = (
                self.db.session_consolidada.query(Watcher)
                .filter_by(
                    repo_id=repo_id,
                    user_id=user_id,
                )
                .first()
            )

            if existing_watcher is None:
                new_watcher = Watcher(
                    repo_id=repo_id,
                    user_id=user_id,
                    ext_ref_id=self.uuid,
                    created_at=watcher.created_at,
                )
                self.db.session_consolidada.add(new_watcher)
                self.db.session_consolidada.commit()

    def add_commit_parents(self, commit_parents: List[CommitParent]):
        for commit_parent in commit_parents:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            commit_id = get_from_map(self.commit_id_map, commit_parent.commit_id)
            parent_id = get_from_map(self.commit_id_map, commit_parent.parent_id)

            # Verifica si el pull request comment ya existe en la base de datos consolidada
            existing_commit_parent = (
                self.db.session_consolidada.query(CommitParent)
                .filter_by(
                    commit_id=commit_id,
                    parent_id=parent_id,
                    ext_ref_id=self.uuid,
                )
                .first()
            )

            if existing_commit_parent is None:
                new_commit_parent = CommitParent(
                    commit_id=commit_id,
                    parent_id=parent_id,
                    ext_ref_id=self.uuid,
                )
                self.db.session_consolidada.add(new_commit_parent)
                self.db.session_consolidada.commit()

    def add_followers(self, followers: List[Follower]):
        for follower in followers:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            user_id = get_from_map(self.user_id_map, follower.user_id)
            follower_id = get_from_map(self.user_id_map, follower.follower_id)

            # Verifica si el pull request comment ya existe en la base de datos consolidada
            existing_follower = (
                self.db.session_consolidada.query(Follower)
                .filter_by(
                    user_id=user_id,
                    follower_id=follower_id,
                )
                .first()
            )

            if existing_follower is None:
                new_follower = Follower(
                    user_id=user_id,
                    follower_id=follower_id,
                    created_at=follower.created_at,
                    ext_ref_id=self.uuid,
                )
                self.db.session_consolidada.add(new_follower)
                self.db.session_consolidada.commit()

    def add_project_members(self, project_members: List[ProjectMember]):
        for project_member in project_members:
            # Obtén el proyecto correspondiente en la base de datos consolidada
            repo_id = get_from_map(self.project_id_map, project_member.repo_id)
            user_id = get_from_map(self.user_id_map, project_member.user_id)

            # Verifica si el pull request comment ya existe en la base de datos consolidada
            existing_project_member = (
                self.db.session_consolidada.query(ProjectMember)
                .filter_by(
                    repo_id=repo_id,
                    user_id=user_id,
                )
                .first()
            )

            if existing_project_member is None:
                new_project_member = ProjectMember(
                    repo_id=repo_id,
                    user_id=user_id,
                    created_at=project_member.created_at,
                    ext_ref_id=self.uuid,
                )
                self.db.session_consolidada.add(new_project_member)
                self.db.session_consolidada.commit()

    def migrate(self):
        users = self.temp.get_users()
        projects = self.temp.get_projects()
        project_members = self.temp.get_project_members()
        labels = self.temp.get_labels()
        milestones = self.temp.get_milestones()

        commits = self.temp.get_commits()
        commit_comments = self.temp.get_commit_comments()
        commit_parents = self.temp.get_commit_parents()

        issues = self.temp.get_issues()
        issue_comments = self.temp.get_issue_comments()
        issue_events = self.temp.get_issue_events()
        issue_labels = self.temp.get_issue_labels()

        prs = self.temp.get_prs()
        pr_comments = self.temp.get_pr_comments()
        pr_history = self.temp.get_pr_history()

        watchers = self.temp.get_watchers()
        followers = self.temp.get_followers()

        logger.info("Migrando usuarios... {uuid}", uuid=self.uuid)
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

        self.add_users(users)
        if len(projects) == 0:
            logger.warning("No hay proyectos para migrar")
            return
        self.add_projects(projects)
        self.add_project_members(project_members)

        self.add_labels(labels)
        self.add_milestones(milestones)

        self.add_watchers(watchers)
        self.add_followers(followers)

        self.add_commits(commits)
        self.add_commit_comments(commit_comments)
        self.add_commit_parents(commit_parents)

        # debug equivalence tables
        pprint(self.user_id_map)
        pprint(self.project_id_map)
        pprint(self.commit_id_map)

        self.add_pull_requests(prs)
        self.add_pull_request_comments(pr_comments)
        self.add_pull_request_history(pr_history)

        self.add_issues(issues)
        self.add_issue_comments(issue_comments)
        self.add_issue_events(issue_events)
        self.add_issue_labels(issue_labels)
