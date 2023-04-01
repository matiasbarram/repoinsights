from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String)
    name = Column(String)
    company = Column(Integer)
    location = Column(String)
    email = Column(String)
    created_at = Column(TIMESTAMP)
    type = Column(String)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    forked_from = Column(Integer)
    url = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))


# class Watcher(Base):
#     __tablename__ = "watchers"

#     id = Column(Integer, primary_key=True)
#     repo_id = Column(Integer, ForeignKey("repositories.id"))
#     user_id = Column(Integer, ForeignKey("users.id"))
#     created_at = Column(DateTime)
#     ext_ref_id = Column(String)

#     user = relationship("User", back_populates="watched_repos")
#     repo = relationship("Repository", back_populates="watchers")
