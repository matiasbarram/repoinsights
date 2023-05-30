from pprint import pprint
from psycopg2.extensions import connection


class MetricDB:
    def __init__(self, conn: connection) -> None:
        self.conn = conn

    def get_metric_id(self, metric_name: str) -> int | None:
        pprint(metric_name)

        with self.conn.cursor() as curs:
            curs.execute(
                """
                    SELECT id FROM metrics 
                    WHERE name = %s
                """,
                (metric_name,),
            )
            result = curs.fetchone()
        return result[0] if result else None

    def check_if_exists(self, extraction_id: int, metric_group) -> bool:
        table_mapping = {
            "developers": "user_metrics",
            "issues": "issue_metrics",
            "pull_requests": "pull_request_metrics",
            "repository": "project_metrics",
        }

        table_name = table_mapping.get(metric_group)

        if not table_name:
            raise ValueError(f"Unknown metric_group: {metric_group}")

        with self.conn.cursor() as curs:
            curs.execute(
                f"""
                SELECT 1 FROM {table_name}
                WHERE extraction_id = %s
                LIMIT 1
                """,
                (extraction_id,),
            )
            result = curs.fetchone()

        return result is not None
