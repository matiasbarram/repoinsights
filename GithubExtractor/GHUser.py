from GithubExtractor.GHRepository import GHRepository
from github import NamedUser, PaginatedList
from helper.utils import format_dt, get_user_type


class GHUser(GHRepository):
    def get_user_data(self, user: NamedUser.NamedUser):
        if user is None:
            return None
        data = {
            "login": user.login,
            "name": user.name,
            "company": user.company,
            "location": user.location,
            "created_at": format_dt(user.created_at),
            "type": get_user_type(user.type),
        }
        print(f"User data {data}")
        return data

    def get_watcher_data(self, watcher: NamedUser.NamedUser):
        data = {"id": watcher.id, "created_at": watcher.created_at}
        print(f"watcher data {data}")
        return data

    def get_member_data(self, member: NamedUser.NamedUser):
        data = {
            "id": member.id,
            "created_at": member.created_at,
            "repo_id": self.repo.id,
        }
        print(f"member data {data}")
        return data

    def get_follower_data(
        self, user: NamedUser.NamedUser, follower: NamedUser.NamedUser
    ):
        data = {
            "follower_id": follower.id,
            "user_id": user.id,
            "created_at": format_dt(follower.created_at),
        }
        print(f"follower data {data}")
        return data

    def get_followers(self, user: NamedUser.NamedUser):
        followers: PaginatedList.PaginatedList[
            NamedUser.NamedUser
        ] = user.get_followers()
        return followers
