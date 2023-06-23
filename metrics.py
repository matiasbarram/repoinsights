import json
from services.metrics_service.calc_controller.calculate import CalculateMetrics
from services.metrics_service.conn import ConsolidadaConnection
from services.metrics_service.load_controller.load import MetricsLoader


def save_results_to_file(results):
    with open("metrics_results.json", "w") as f:
        json_dump = json.dumps(results)
        f.write(json_dump)


def main():
    consolidada_conn = ConsolidadaConnection()
    conn = consolidada_conn.get_connection()
    projects = consolidada_conn.get_all_projects()
    for project in projects:
        extraction_id, project_id = project
        calc_metrics = CalculateMetrics(conn, project_id, extraction_id)
        load_metrics = MetricsLoader(conn, project_id, extraction_id)
        results = calc_metrics.calculate_metrics()

        save_results_to_file(results)

        for metric_group in calc_metrics.metrics:
            load_metrics.add_metric_group(metric_group)
        load_metrics.load_metrics(results)


if __name__ == "__main__":
    main()
