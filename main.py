from sqlalchemy.orm import sessionmaker, aliased
from DWConnector.orm_main import DWConnector
from DWConnector.models.models import Project, Commit, PullRequest, User, Issue
from sqlalchemy import create_engine, func

dw_connector = DWConnector()
engine = dw_connector.engine

Session = sessionmaker(bind=engine)
session = Session()

query = (
    session.query(
        PullRequest,
        User.login,
        aliased(Project, name="head_project_name"),
        aliased(Project, name="base_project_name"),
        aliased(Commit, name="head_commit_sha"),
        aliased(Commit, name="base_commit_sha"),
    )
    .join(User, PullRequest.user_id == User.id)
    .join(
        aliased(Project, name="head_project"),
        PullRequest.head_repo_id == aliased(Project, name="head_project").id,
    )
    .join(
        aliased(Project, name="base_project"),
        PullRequest.base_repo_id == aliased(Project, name="base_project").id,
    )
    .join(
        aliased(Commit, name="head_commit"),
        PullRequest.head_commit_id == aliased(Commit, name="head_commit").id,
    )
    .join(
        aliased(Commit, name="base_commit"),
        PullRequest.base_commit_id == aliased(Commit, name="base_commit").id,
    )
)

# Imprimir resultados
for (
    pr,
    user_login,
    head_project_name,
    base_project_name,
    head_commit_sha,
    base_commit_sha,
) in query.all():
    print(
        f"Pull Request #{pr.id}: {user_login} | {head_project_name} -> {base_project_name} | {head_commit_sha} -> {base_commit_sha}"
    )

# Cerrar sesión
session.close()
