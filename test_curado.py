import pika
from CurateRepos.main import CurateMetrics
from pprint import pprint
from datetime import datetime

project = "apache/airflow"

curate_metrics = CurateMetrics(project)
core_contributors = curate_metrics.core_contributors_metric()
# pprint(core_contributors)

# meses incluidos en el calculo
start_date = datetime.strptime("2021-07", "%Y-%m")
end_month = datetime.strptime("2023-04", "%Y-%m")
commit_frecuency = curate_metrics.commit_frecuency_metric(start_date, end_month)
print(commit_frecuency)
