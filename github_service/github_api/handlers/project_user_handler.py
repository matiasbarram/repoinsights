from github.Repository import Repository
from github.NamedUser import NamedUser
from ..user import GHUser


class ProjectUserHandler:
    def __init__(self, repo: Repository):
        self.repo = repo

    def get_members(self):
        print("Getting members")
        members = self.repo.get_contributors()
        return [GHUser(member) for member in members]

    def get_watchers(self):
        print("Getting watchers")
        watchers = self.repo.get_watchers()
        return [GHUser(watcher) for watcher in watchers]

    def get_owner(self):
        print("Getting owner")
        owner = self.repo.owner
        return GHUser(owner)
