from services.metrics_service.conn import ConsolidadaConnection
from services.metrics_service.load import MetricsLoader
import os
from pprint import pprint
from typing import Dict, List, Tuple, Any
import glob
from loguru import logger
from .helper import yaml_to_dict, files_in_dir

CONSOLIDADA_USER = os.environ["CONSOLIDADA_USER"]
CONSOLIDADA_PASSWORD = os.environ["CONSOLIDADA_PASS"]
CONSOLIDADA_DATABASE = os.environ["CONSOLIDADA_DB"]
CONSOLIDADA_IP = os.environ["CONSOLIDADA_IP"]
CONSOLIDADA_PORT = os.environ["CONSOLIDADA_PORT"]


class InsightsMetrics:
    def __init__(self, project_id: int) -> None:
        self.conn = self.connect_to_consolidada()
        self.project_id = project_id

    def get_metrics(self, metrics_files):
        metrics = [yaml_to_dict(file) for file in metrics_files]
        return metrics

    def connect_to_consolidada(self):
        conn = ConsolidadaConnection(
            host=CONSOLIDADA_IP,
            port=CONSOLIDADA_PORT,
            database=CONSOLIDADA_DATABASE,
            user=CONSOLIDADA_USER,
            password=CONSOLIDADA_PASSWORD,
        )

        return conn.get_connection()

    def get_metrics_files(self):
        path = os.path.dirname(os.path.abspath(__file__)) + "/metrics/"
        metrics = files_in_dir(path, "yml")
        return metrics

    def generate_params(self, metric: Dict, project_id: int):
        params = []
        if metric.get("variables"):
            for variable in metric["variables"]:
                if variable == "project_id":
                    params.append(project_id)
                else:
                    logger.error(f"Variable {variable} not supported")
                    raise Exception("Variable not supported")
        else:
            params.append(project_id)
        return params

    def calculate_metrics(self):
        metrics_files = self.get_metrics_files()
        metrics = self.get_metrics(metrics_files)
        results = {}
        with self.conn.cursor() as curs:
            metric: Dict[str, Any]
            for metric in metrics:  # type: ignore
                params = self.generate_params(metric, self.project_id)
                curs.execute(metric["metric"], params)
                data = curs.fetchall()
                field_names = [desc[0] for desc in curs.description]
                results[metric["name"]] = {"results": data, "col_names": field_names}
        return results

    def load_metrics(self, results: Dict[str, List[Tuple]]):
        metrics_loader = MetricsLoader(self.conn, self.project_id)
        metrics_loader.load_metrics(results)
