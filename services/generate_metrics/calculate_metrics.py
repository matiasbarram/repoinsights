from services.generate_metrics.consolidada_conn import ConsolidadaConnection
from services.generate_metrics.loader_metrics import MetricsLoader
import os
from pprint import pprint

from typing import Dict, List, Tuple
import json

from services.generate_metrics.metrics.hero_project import hero_project_query
from services.generate_metrics.metrics.number_of_developers import nod
from services.generate_metrics.metrics.maintenance_type import maintenance_type


CONSOLIDADA_USER = os.environ["CONSOLIDADA_USER"]
CONSOLIDADA_PASSWORD = os.environ["CONSOLIDADA_PASS"]
CONSOLIDADA_DATABASE = os.environ["CONSOLIDADA_DB"]
CONSOLIDADA_IP = os.environ["CONSOLIDADA_IP"]
CONSOLIDADA_PORT = os.environ["CONSOLIDADA_PORT"]


class InsightsMetrics:
    def __init__(self, project_id: int) -> None:
        self.conn = self.connect_to_consolidada()
        self.project_id = project_id

        self.jsonb_attrs = {
            "int",
            "float",
            "string",
            "boolean",
        }

    def connect_to_consolidada(self):
        conn = ConsolidadaConnection(
            host=CONSOLIDADA_IP,
            port=CONSOLIDADA_PORT,
            database=CONSOLIDADA_DATABASE,
            user=CONSOLIDADA_USER,
            password=CONSOLIDADA_PASSWORD,
        )

        return conn.get_connection()

    def calculate_metrics(self):
        results = {}
        with self.conn.cursor() as curs:
            curs.execute(hero_project_query, [self.project_id])
            hero_project = curs.fetchall()
            results["hero_project"] = hero_project

            curs.execute(nod, [self.project_id])
            number_of_developers = curs.fetchall()
            results["number_of_developers"] = number_of_developers

            curs.execute(maintenance_type, [self.project_id])
            maintenance_type_result = curs.fetchall()
            results["maintenance_type"] = maintenance_type_result

        return results

    def load_metrics(self, results: Dict[str, List[Tuple]]):
        metrics_loader = MetricsLoader(self.conn, self.project_id)
        metrics_loader.load_metrics(results)
