from typing import Dict, List, Tuple, Union
import json
from pprint import pprint
from psycopg2.extensions import connection


class MetricsLoader:
    def __init__(self, conn: connection, project_id):
        self.conn = conn
        self.project_id = project_id

    def get_metrics_map(self) -> Dict[str, int]:
        with self.conn.cursor() as curs:
            curs.execute("SELECT id, name FROM metrics")
            metrics = curs.fetchall()
            return {metric_name: metric_id for metric_id, metric_name in metrics}

    def format_to_jsonb(self, value) -> dict:
        val_type = type(value).__name__
        return {"type": val_type, "value": value}

    def get_metric_result(self, result: Tuple) -> Tuple[int | None, dict | None]:
        repo_id, value = result
        return repo_id, self.format_to_jsonb(value) if result else (None, None)  # type: ignore

    def insert_metric_value(
        self, repo_id: int | None, metric_id: int | None, value: dict | None
    ) -> None:
        json_value = json.dumps(value)
        with self.conn.cursor() as curs:
            curs.execute(
                "INSERT INTO metrics_log (repo_id, metric_id, value) VALUES (%s, %s, %s)",
                (repo_id, metric_id, json_value),
            )

    def load_metrics(self, results: Dict[str, List[Tuple]]) -> None:
        metrics_id = self.get_metrics_map()
        for metric_name, metric_values in results.items():
            metric_id = metrics_id[metric_name]
            print(f"Metric: {metric_name}, ID: {metric_id}, values: {metric_values}")
            if not metric_values:
                value = self.format_to_jsonb(None)
                pprint(
                    {"repo_id": self.project_id, "metric_id": metric_id, "value": value}
                )
                self.insert_metric_value(self.project_id, metric_id, value)
            else:
                for value_list in metric_values:
                    repo_id, value = self.get_metric_result(value_list)
                    pprint({"repo_id": repo_id, "metric_id": metric_id, "value": value})
                    self.insert_metric_value(repo_id, metric_id, value)

        self.conn.commit()
