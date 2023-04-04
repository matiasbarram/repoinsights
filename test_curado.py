import pika
from CurateRepos.main import CurateMetrics
from pprint import pprint

project = "openai/triton"

curate_metrics = CurateMetrics(project)
core_contributors = curate_metrics.core_contributors_metric()
pprint(core_contributors)
