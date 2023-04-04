"""
Traceback (most recent call last):
  File "/home/matias/proyecto/repoinsights/main.py", line 175, in <module>
    for comment in comments:
  File "/home/matias/.local/share/virtualenvs/repoinsights-zOXF-EYI/lib/python3.10/site-packages/github/PaginatedList.py", line 56, in __iter__
    newElements = self._grow()
  File "/home/matias/.local/share/virtualenvs/repoinsights-zOXF-EYI/lib/python3.10/site-packages/github/PaginatedList.py", line 67, in _grow
    newElements = self._fetchNextPage()
  File "/home/matias/.local/share/virtualenvs/repoinsights-zOXF-EYI/lib/python3.10/site-packages/github/PaginatedList.py", line 201, in _fetchNextPage
    headers, data = self.__requester.requestJsonAndCheck(
  File "/home/matias/.local/share/virtualenvs/repoinsights-zOXF-EYI/lib/python3.10/site-packages/github/Requester.py", line 398, in requestJsonAndCheck
    return self.__check(
  File "/home/matias/.local/share/virtualenvs/repoinsights-zOXF-EYI/lib/python3.10/site-packages/github/Requester.py", line 423, in __check
    raise self.__createException(status, responseHeaders, output)
github.GithubException.RateLimitExceededException: 403 {"message": "API rate limit exceeded for user ID 64421508.", "documentation_url": "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting"}
"""


from dotenv import load_dotenv
from github import (
    NamedUser,
    Repository,
    PullRequest,
    Github,
    PaginatedList,
    NamedUser,
    PullRequestComment,
    IssueComment,
)
import DWConnector.main as DWService
from typing import Union, List, Dict, Any
from GithubExtractor.GHExtractor import GHExtractor
from GithubExtractor.GHGetToken import GHGetToken

load_dotenv()


# dw_connector = DWService.DWConnector()
# repos = dw_connector.get_repos()
# # enqueue_repos(repos)


repos = [
    "ericblade/quagga2",  # ADDED BY ME  # ADDED BY ME
    "geohot/corona",  # ADDED BY ME  # ADDED BY ME
    "mongodb/mongo",
    "rstudio/shiny",
    "facebook/folly",  # TODO check if user exist when get get_commit_data
    "mavam/stat-cookbook",
    "akka/akka",
    "hadley/devtools",
    "johnmyleswhite/ProjectTemplate",
    "facebook/hiphop-php",
    "yihui/knitr",
    "TTimo/doom3.gpl",
    "ariya/phantomjs",
    "TrinityCore/TrinityCore",
    "mangos/MaNGOS",
    "bitcoin/bitcoin",
    "keithw/mosh",
    "xbmc/xbmc",
    "joyent/http-parser",
    "kr/beanstalkd",
    "antirez/redis",
    "liuliu/ccv",
    "memcached/memcached",
    "openframeworks/openFrameworks",
    "libgit2/libgit2",
    "vmg/redcarpet",
    "joyent/libuv",
    "SignalR/SignalR",
    "hbons/SparkleShare",
    "moxiecode/plupload",
    "mono/mono",
    "NancyFx/Nancy",
    "ServiceStack/ServiceStack",
    "AutoMapper/AutoMapper",
    "restsharp/RestSharp",
    "ravendb/ravendb",
    "SamSaffron/MiniProfiler",
    "nathanmarz/storm",
    "elasticsearch/elasticsearch",
    "JakeWharton/ActionBarSherlock",
    "facebook/facebook-android-sdk",
    "clojure/clojure",
    "Bukkit/CraftBukkit",
    "netty/netty",
    "github/android",
    "joyent/node",
    "jquery/jquery",
    "h5bp/html5-boilerplate",
    "bartaz/impress.js",
    "mbostock/d3",
    "harvesthq/chosen",
    "FortAwesome/Font-Awesome",
    "mrdoob/three.js",
    "zurb/foundation",
    "symfony/symfony",
    "EllisLab/CodeIgniter",
    "facebook/php-sdk",
    "zendframework/zf2",
    "cakephp/cakephp",
    "ginatrapani/ThinkUp",
    "sebastianbergmann/phpunit",
    "codeguy/Slim",
    "django/django",
    "facebook/tornado",
    "jkbr/httpie",
    "mitsuhiko/flask",
    "kennethreitz/requests",
    "xphere-forks/symfony",
    "reddit/reddit",
    "boto/boto",
    "django-debug-toolbar/django-debug-toolbar",
    "midgetspy/Sick-Beard",
    "divio/django-cms",
    "rails/rails",
    "mxcl/homebrew",
    "mojombo/jekyll",
    "gitlabhq/gitlabhq",
    "diaspora/diaspora",
    "plataformatec/devise",
    "joshuaclayton/blueprint-css",
    "imathis/octopress",
    "vinc/vinc.cc",
    "thoughtbot/paperclip",
    "chriseppstein/compass",
    "twitter/finagle",
    "robey/kestrel",
    "twitter/flockdb",
    "twitter/gizzard",
    "sbt/sbt",
    "scala/scala",
    "scalatra/scalatra",
    "twitter/zipkin",
    "Craftbukkit/Bukkit",
]

gh_token = GHGetToken()


# TODO
# connector = RabbitMQConnector()
# connector.get_repo_from_queue()
def get_repo_from_queue(repos) -> str:
    return repos[0]


repo = get_repo_from_queue(repos)
print(repo)
gh_extractor = GHExtractor(gh_token, repo)
owner: NamedUser.NamedUser = gh_extractor.get_project_owner()

gh_extractor.get_user_data(owner)
watchers: PaginatedList.PaginatedList = gh_extractor.get_watchers()
print("---------WATCHERS----------")
for watcher in watchers:
    gh_extractor.get_watcher_data(watcher)
    gh_extractor.get_user_data(watcher)
    break

print("---------MEMBERS----------")
members = gh_extractor.get_members()
try:
    for member in members:
        gh_extractor.get_member_data(member)
        gh_extractor.get_user_data(member)
        break
except Exception as e:
    print("No fue posible obtener los miembros del proyecto")

print("---------REPO LABELS--------")
labels = gh_extractor.get_project_labels()
for label in labels:
    gh_extractor.get_label_data(label)
    break

print("---------REPO MILESTONES----------")
milestones = gh_extractor.get_milestones()
for milestone in milestones:
    gh_extractor.get_milestone_data(milestone)
    break


print("---------ISSUES----------")
issues = gh_extractor.get_issues()
for issue in issues:
    gh_extractor.get_issue_data(issue)
    print("---------ISSUE LABELS----------")
    gh_extractor.get_issue_labels(issue)
    for label in issue.labels:
        gh_extractor.get_label_data(label)
    print("---------ISSUE COMMENTS----------")
    issue_comments = gh_extractor.get_issue_comments(issue)
    issue_comment: IssueComment.IssueComment
    for issue_comment in issue_comments:
        gh_extractor.get_issue_comment_data(issue, issue_comment)
        gh_extractor.get_user_data(issue_comment.user)
    print("---------ISSUE EVENTS--------------------")
    events = gh_extractor.get_issue_events(issue)
    for event in events:
        gh_extractor.get_issue_event_data(issue, event)
        gh_extractor.get_user_data(event.actor)
    break

print("---------COMMITS----------")
# TODO order of commits
commits = gh_extractor.get_commits()
for commit in commits:
    try:
        gh_extractor.get_commit_data(commit)
        gh_extractor.get_user_data(commit.author)
    except Exception as e:
        print("No fue posible obtener información del commit")
    print("---------COMMITS PARENTS----------")
    parents_commits = gh_extractor.get_commit_parents(commit)
    for parent_commit in parents_commits:
        gh_extractor.get_commit_data(parent_commit)
        gh_extractor.get_user_data(parent_commit.author)
    print("---------COMMITS COMMENTS----------")
    # TODO revisar
    issue_comments = gh_extractor.get_commit_comments(commit)
    for commit_comment in issue_comments:
        gh_extractor.get_commit_comment_data(commit_comment)
        gh_extractor.get_user_data(commit_comment.user)
    break

print("---------PULL REQUESTS----------")

pulls = gh_extractor.get_pulls()
pull: PullRequest.PullRequest
for pull in pulls:
    pr_assignee = pull.assignee if pull.assignee is not None else None
    data = gh_extractor.get_pull_data(pull)
    gh_extractor.get_user_data(pull.user)
    if pr_assignee is not None:
        gh_extractor.get_user_data(pr_assignee)
    print("---------PULL REQUESTS COMMENTS----------")
    comments = gh_extractor.get_pull_comments(pull)
    comment: PullRequestComment.PullRequestComment
    for comment in comments:
        gh_extractor.get_pull_comment_data(pull, comment)
        gh_extractor.get_user_data(comment.user)
    break
