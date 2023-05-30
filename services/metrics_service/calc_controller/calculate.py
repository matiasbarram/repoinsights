import os
from pprint import pprint
from typing import Dict, Any, List, Tuple
import glob
from loguru import logger
from psycopg2.extensions import connection, cursor
from decimal import Decimal

from ..helper import yaml_to_dict
from ..commons import METRICS_DIR, METRICS_GROUPS
from .metric_validator import MetricValidator
from .metric_extractor import MetricExtractor
from .metric_db import MetricDB


class CalculateMetrics:
    def __init__(self, conn: connection, project_id: int, extraction_id: int) -> None:
        self.project_id = project_id
        self.conn = conn
        self.extraction_id = extraction_id
        self.db = MetricDB(conn)
        self.metrics = MetricExtractor.get_metrics()

    def calculate_metrics(self):
        results = {}
        with self.conn.cursor() as curs:
            valid_groups = MetricValidator.validate_metrics_groups(
                self.extraction_id, self.db.check_if_exists
            )
            for metric in self.metrics:
                metric_group, metrics = metric["group"], metric["metrics"]
                exist = self.db.check_if_exists(self.extraction_id, metric_group)
                if not exist and metric_group in valid_groups:
                    group_metrics = MetricExtractor.calc_metrics_group(
                        metrics, self.project_id, curs
                    )
                    results.update(group_metrics)
                else:
                    logger.warning(
                        f"Metrics for group {metric_group} already exist for extraction_id {self.extraction_id}"
                    )
        return results
