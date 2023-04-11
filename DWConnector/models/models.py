from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    DateTime,
    Boolean,
    DECIMAL,
    Index,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(255), nullable=False)
    name = Column(String(255))
    company = Column(String(255))
    location = Column(String(255))
    email = Column(String(255))
    created_at = Column(TIMESTAMP, nullable=False)
    ext_ref_id = Column(String(24), nullable=False, default="0")
    type = Column(String(255), nullable=False, default="USR")

    projects = relationship("Project", back_populates="owner")
    authored_commits = relationship(
        "Commit", foreign_keys="Commit.author_id", back_populates="author"
    )
    committed_commits = relationship(
        "Commit", foreign_keys="Commit.committer_id", back_populates="committer"
    )
    pull_requests = relationship("PullRequest", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255))
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255), index=True)
    description = Column(String(255))
    language = Column(String(255))
    created_at = Column(
        DateTime, default=datetime.utcnow, server_default=text("CURRENT_TIMESTAMP")
    )
    ext_ref_id = Column(String(24), nullable=False, server_default="0")
    forked_from = Column(Integer, ForeignKey("projects.id"), nullable=True)
    deleted = Column(Boolean, nullable=False, default=False)

    owner = relationship("User", back_populates="projects")
    forks = relationship("Project", back_populates="parent")
    parent = relationship("Project", remote_side=[id], back_populates="forks")
    commits = relationship("Commit", back_populates="project")
    head_pull_requests = relationship(
        "PullRequest",
        foreign_keys="PullRequest.head_repo_id",
        back_populates="head_repo",
    )
    base_pull_requests = relationship(
        "PullRequest",
        foreign_keys="PullRequest.base_repo_id",
        back_populates="base_repo",
    )


class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True)
    head_repo_id = Column(Integer, ForeignKey("projects.id"))
    base_repo_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    head_commit_id = Column(Integer, ForeignKey("commits.id"))
    base_commit_id = Column(Integer, ForeignKey("commits.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pullreq_id = Column(Integer, nullable=False)
    intra_branch = Column(Boolean, nullable=False)
    merged = Column(Boolean, nullable=False, default=False)

    head_repo = relationship(
        "Project", foreign_keys=[head_repo_id], back_populates="head_pull_requests"
    )
    base_repo = relationship(
        "Project", foreign_keys=[base_repo_id], back_populates="base_pull_requests"
    )
    head_commit = relationship("Commit", foreign_keys=[head_commit_id])
    base_commit = relationship("Commit", foreign_keys=[base_commit_id])
    user = relationship("User", back_populates="pull_requests")


class Commit(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True)
    sha = Column(String(40), unique=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    committer_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_at = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    ext_ref_id = Column(String(24), nullable=False, server_default="0")

    author = relationship(
        "User", foreign_keys=[author_id], back_populates="authored_commits"
    )
    committer = relationship(
        "User", foreign_keys=[committer_id], back_populates="committed_commits"
    )
    project = relationship("Project", back_populates="commits")
