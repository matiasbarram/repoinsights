from typing import Any, Dict, Tuple
from psycopg2.extensions import connection
from loguru import logger
from pprint import pprint
from ..commons import TABLE_NAME_MAP


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
        extraction_id: int,
    ):
        logger.warning(result)
        table_info = TABLE_NAME_MAP.get(group_name)
        if table_info is None:
            raise ValueError(f"Unknown group_name: {group_name}")

        table_name = table_info["table"]
        params = table_info["params"]
        results = list(result)
        results.pop(0)
        results.insert(0, extraction_id)
        results.insert(0, metric_id)
        placeholders = ", ".join(["%s"] * len(results))
        params_query = ", ".join(params)

        query = f"INSERT INTO {table_name} ({params_query}) VALUES ({placeholders})"
        logger.debug("{query}, {results}", query=query, results=results)
        pprint(
            {
                "query": query,
                "results": results,
                "table_name": table_name,
                "params_query": params_query,
                "placeholders": placeholders,
            }
        )
        with self.conn.cursor() as curs:
            curs.execute(query, results)
            self.conn.commit()
