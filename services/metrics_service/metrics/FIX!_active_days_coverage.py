active_days_coverage = """
WITH
    total_days AS (
        SELECT DATE '2013-01-31' - DATE '2013-01-01' + 1 AS total_days
    ),
    active_days AS (
        SELECT
            COUNT(DISTINCT DATE(c.created_at)) AS active_days
        FROM
            commits c
            INNER JOIN projects r ON c.project_id = r.id
        WHERE
            r.id = 1 AND
            c.created_at >= DATE '2013-01-01' AND
            c.created_at <= DATE '2013-01-31'
    )
SELECT
    active_days.active_days,
    total_days.total_days,
    (active_days.active_days * 1.0) / total_days.total_days AS active_days_coverage
FROM
    total_days, active_days;
"""
