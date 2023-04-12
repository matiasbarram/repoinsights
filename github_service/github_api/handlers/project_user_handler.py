from github.Repository import Repository
from github.NamedUser import NamedUser
from ..user import GHUser
from datetime import datetime
from typing import List


class ProjectUserHandler:
    def __init__(self, repo: Repository):
        self.repo = repo

    def get_members(self, since=None, until=None):
        members = self.repo.get_contributors()
        if since and until:
            return [
                GHUser(member)
                for member in members
                if since <= member.created_at <= until
            ]
        return [GHUser(member) for member in members]

    def get_watchers(self, since=None, until=None):
        watchers = self.repo.get_watchers()
        if since and until:
            return [
                GHUser(watcher)
                for watcher in watchers
                if since <= watcher.created_at <= until
            ]
        return [GHUser(watcher) for watcher in watchers]

    def get_stargazers(self, since=None, until=None) -> List[GHUser]:
        stargazers = self.repo.get_stargazers_with_dates()
        if since and until:
            return [
                GHUser(stargazer.user)
                for stargazer in stargazers
                if since <= stargazer.starred_at <= until
            ]
        return [GHUser(stargazer.user) for stargazer in stargazers]

    def get_owner(self):
        owner = self.repo.owner
        return GHUser(owner)
