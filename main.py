from dotenv import load_dotenv
from github import NamedUser, Repository, PullRequest, Github, PaginatedList, NamedUser
import DWConnector.main as DWService
from GithubExtractor.main import GHTokenUser, GHExtractor

load_dotenv()


# dw_connector = DWService.DWConnector()
# repos = dw_connector.get_repos()
# # enqueue_repos(repos)


repos = [
    "rstudio/shiny",
    "facebook/folly",  # TODO check if user exist when get get_commit_data
    "mavam/stat-cookbook",
    "akka/akka",
    "hadley/devtools",
    "johnmyleswhite/ProjectTemplate",
    "facebook/hiphop-php",
    "yihui/knitr",
    "mongodb/mongo",
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

gh_user = GHTokenUser()


# TODO
# connector = RabbitMQConnector()
# connector.get_repo_from_queue()
def get_repo_from_queue() -> str:
    for repo in repos:
        return repo


repo = get_repo_from_queue()
print(repo)
gh_extractor = GHExtractor(gh_user, repo)
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
labels = gh_extractor.get_labels(gh_extractor.repo)
for label in labels:
    gh_extractor.get_label_data(label)
    break

print("---------ISSUES----------")
issues = gh_extractor.get_issues()
for issue in issues:
    gh_extractor.get_issue_data(issue)
    print("---------ISSUE LABELS----------")
    gh_extractor.get_labels(issue)
    for label in issue.labels:
        gh_extractor.get_label_data(label)
    print("---------ISSUE COMMENTS----------")
    comments = gh_extractor.get_issue_comments(issue)
    for comment in comments:
        gh_extractor.get_issue_comment_data(comment)
        gh_extractor.get_user_data(comment.user)
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
    comments = gh_extractor.get_commit_comments(commit)
    for comment in comments:
        gh_extractor.get_commit_comment_data(comment)
        gh_extractor.get_user_data(comment.user)
    break
