import os
from pprint import pprint
from typing import Dict, Any, List, Tuple
import glob
from loguru import logger
from psycopg2.extensions import connection, cursor
from decimal import Decimal

from .helper import yaml_to_dict
from .commons import METRICS_DIR, METRICS_GROUPS


class CalculateMetrics:
    def __init__(self, conn: connection, project_id: int) -> None:
        self.project_id = project_id
        self.conn = conn

    def get_metrics(self) -> List[Dict[str, Any]]:
        metrics = []
        for metrics_group in METRICS_GROUPS:
            group = {"group": metrics_group, "metrics": []}
            dirs = glob.glob(METRICS_DIR + metrics_group + "/*.yml")
            group["metrics"] = [yaml_to_dict(dir) for dir in dirs]
            metrics.append(group)
        return metrics

    def generate_params(self, metric: Dict, project_id: int):
        if metric.get("variables"):
            params = []
            variables = metric["variables"]
            for var in variables:
                if var == "project_id":
                    params.append(project_id)
            return params
        return [project_id]

    def convert_if_decimal(self, item: Tuple[Any]):
        data = list(item)
        for i in range(len(data)):
            if isinstance(data[i], Decimal):
                data[i] = float(data[i])
        return data

    def calc_metrics_group(self, metrics: List[Dict], curs: cursor):
        def get_result(data):
            if data is None:
                raise ValueError("Metric not found")
            elif len(data) == 0:
                return None
            else:
                result = [self.convert_if_decimal(item) for item in data]
            return result

        results = {}
        for metric in metrics:
            params = self.generate_params(metric, self.project_id)
            curs.execute(metric["metric"], params)
            data = curs.fetchall()
            result = get_result(data)
            if result is None:
                continue
            results[metric["name"]] = result

        return results

    def calculate_metrics(self):
        metrics = self.get_metrics()
        results = {}
        with self.conn.cursor() as curs:
            for metric in metrics:
                _, metrics = metric["group"], metric["metrics"]
                group_metrics = self.calc_metrics_group(metrics, curs)
                results.update(group_metrics)
        return results
