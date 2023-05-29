import json
import os
from pprint import pprint

from services.metrics_service.calculate import CalculateMetrics
from services.metrics_service.conn import ConsolidadaConnection
from services.metrics_service.load import MetricsLoader


def save_results_to_file(results):
    with open("metrics_results.json", "w") as f:
        json_dump = json.dumps(results)
        f.write(json_dump)


def main(project_id):
    consolidada_conn = ConsolidadaConnection()
    conn = consolidada_conn.get_connection()

    calc_metrics = CalculateMetrics(conn, project_id)
    load_metrics = MetricsLoader(conn, project_id)

    metrics = calc_metrics.get_metrics()
    results = calc_metrics.calculate_metrics()

    save_results_to_file(results)

    for metric_group in metrics:
        load_metrics.add_metric_group(metric_group)
    load_metrics.load_metrics(results)


if __name__ == "__main__":
    main(1)