from github import NamedUser
from helper.utils import format_dt, get_user_type


class GHUser:
    def get_user_data(self, user: NamedUser.NamedUser):
        data = {
            "login": user.login,
            "name": user.name,
            "company": user.company,
            "location": user.location,
            "created_at": format_dt(user.created_at),
            "type": get_user_type(user.type),
        }
        print(f"User data {data}")

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
