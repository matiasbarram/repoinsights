import pika
from CurateRepos.main import CurateMetrics


project = "openai/triton"

curate_metrics = CurateMetrics(project)
curate_metrics.core_contributors_metrics()
