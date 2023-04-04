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


import pika
import sys

credentials = pika.PlainCredentials("user", "password")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
channel = connection.channel()
queue_name = "projects_test"
channel.queue_declare(
    queue=queue_name, durable=True, exclusive=False, auto_delete=False
)

try:
    for repo in repos:
        message = repo
        # Send a message
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                content_type="text/plain", delivery_mode=pika.DeliveryMode.Persistent
            ),
            mandatory=True,
        )
        print("Message was published")
        break

except pika.exceptions.UnroutableError:  # type: ignore
    print("Message was returned")

connection.close()
