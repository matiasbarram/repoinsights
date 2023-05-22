pr_closure_ratio = """
WITH opened_prs AS (
    SELECT
        COUNT(*) AS opened_count
    FROM
        pull_request_history prh_opened
        INNER JOIN pull_requests pr ON prh_opened.pull_request_id = pr.id
    WHERE
        pr.base_repo_id = %s AND
        prh_opened.action = 'opened' AND
        prh_opened.created_at BETWEEN '2013-01-01' AND '2013-10-31' AND
        NOT EXISTS (
            SELECT 1
            FROM
                pull_request_history prh_closed
            WHERE
                prh_closed.pull_request_id = pr.id AND
                (prh_closed.action = 'closed' OR prh_closed.action = 'merged') AND
                prh_closed.created_at BETWEEN '2013-01-01' AND '2013-10-31'
        )
),
closed_prs AS (
    SELECT
        COUNT(*) AS closed_count
    FROM
        pull_request_history prh
        INNER JOIN pull_requests pr ON prh.pull_request_id = pr.id
    WHERE
        pr.base_repo_id = %s AND
        (prh.action = 'closed' OR prh.action = 'merged') AND
        prh.created_at BETWEEN '2013-01-01' AND '2013-10-31'
)

SELECT
    opened_prs.opened_count,
    closed_prs.closed_count,
    (opened_prs.opened_count::numeric / NULLIF(closed_prs.closed_count, 0)) AS open_to_closed_ratio
FROM
    opened_prs, closed_prs;
"""
