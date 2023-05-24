from typing import Dict, List, Any, Tuple
import json
from pprint import pprint
from loguru import logger
from psycopg2.extensions import connection
from .commons import TABLE_NAME_MAP


class Metric:
    def __init__(self, metric: Dict[str, Any], conn: connection):
        self.conn = conn
        self.name = metric["name"]
        self.description = metric.get("description")
        self.measurement_type = metric.get("measurement")
        self.id = self._get_or_create_id()

    def _get_or_create_id(self):
        with self.conn.cursor() as curs:
            curs.execute(
                """
                INSERT INTO metrics (name, description, measurement_type) VALUES (%s, %s, %s) 
                ON CONFLICT (name) DO UPDATE
                SET description = EXCLUDED.description, measurement_type = EXCLUDED.measurement_type 
                RETURNING id
                """,
                (self.name, self.description, self.measurement_type),
            )
            result = curs.fetchone()

            if result is None:
                curs.execute("SELECT id FROM metrics WHERE name = %s", (self.name,))
                result = curs.fetchone()
                if result:
                    result = result[0]
            self.conn.commit()
        return result[0] if result else None

    def load(
        self,
        group_name: str,
        metric_id: int,
        result: Tuple[Any],
    ):
        logger.warning(result)
        table_info = TABLE_NAME_MAP.get(group_name)
        if table_info is None:
            raise ValueError(f"Unknown group_name: {group_name}")

        table_name = table_info["table"]
        params = table_info["params"]
        results = [metric_id] + list(result)
        placeholders = ", ".join(["%s"] * len(results))
        params_query = ", ".join(params)

        query = f"INSERT INTO {table_name} ({params_query}) VALUES ({placeholders})"
        logger.debug("{query}, {results}", query=query, results=results)
        with self.conn.cursor() as curs:
            curs.execute(query, results)
            self.conn.commit()


class MetricGroup:
    def __init__(self, group: Dict[str, Any], conn: connection):
        self.name = group["group"]
        self.metrics = [Metric(metric, conn) for metric in group["metrics"]]

    def get_metrics_ids(self):
        return [{"name": metric.name, "id": metric.id} for metric in self.metrics]


class MetricsLoader:
    def __init__(self, conn: connection, project_id):
        self.conn = conn
        self.project_id = project_id
        self.metric_groups: List[MetricGroup] = []

    def add_metric_group(self, group: Dict[str, Any]):
        self.metric_groups.append(MetricGroup(group, self.conn))

    def load_metrics(self, results: Dict):
        for group in self.metric_groups:
            self._load_metrics_for_group(group, results)

    def _load_metrics_for_group(self, group: MetricGroup, results: Dict):
        metrics_ids = group.get_metrics_ids()
        for metric in metrics_ids:
            self._load_metric_results(metric, results)

    def _load_metric_results(self, metric: Dict[str, Any], results: Dict):
        metric_results = results.get(metric["name"])
        if metric_results is None:
            return
        for metric_result in metric_results:
            self._log_and_load_metric_result(metric_result, metric)

    def _log_and_load_metric_result(
        self, metric_result: List[Any], metric: Dict[str, Any]
    ):
        self._load_metric_result_to_database(metric["id"], metric_result)

    def _load_metric_result_to_database(self, metric_id: int, result):
        for group in self.metric_groups:
            for m in group.metrics:
                if m.id == metric_id:
                    m.load(group.name, metric_id, result)
                    return
