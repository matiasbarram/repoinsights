\connect ghtorrent_restore_2015


CREATE VIEW public_projects AS
SELECT *
FROM ghtorrent_restore_2015.projects
WHERE NOT deleted AND NOT private;

CREATE VIEW public_commits AS
SELECT commits.*
FROM ghtorrent_restore_2015.commits
JOIN public_projects ON commits.project_id = public_projects.id;

CREATE VIEW public_project_commits AS
SELECT project_commits.*
FROM ghtorrent_restore_2015.project_commits
JOIN public_projects ON project_commits.project_id = public_projects.id;

CREATE VIEW public_project_members AS
SELECT project_members.*
FROM ghtorrent_restore_2015.project_members
JOIN public_projects ON project_members.repo_id = public_projects.id;

CREATE VIEW public_extractions AS
SELECT extractions.*
FROM ghtorrent_restore_2015.extractions
JOIN public_projects ON extractions.project_id = public_projects.id;

CREATE VIEW public_project_metrics AS
SELECT project_metrics.*
FROM ghtorrent_restore_2015.project_metrics
JOIN ghtorrent_restore_2015.extractions ON project_metrics.extraction_id = extractions.id
JOIN public_projects ON extractions.project_id = public_projects.id;


CREATE VIEW public_commit_comments AS
SELECT commit_comments.*
FROM ghtorrent_restore_2015.commit_comments
JOIN public_commits ON commit_comments.commit_id = public_commits.id;

CREATE VIEW public_commit_parents AS
SELECT commit_parents.*
FROM ghtorrent_restore_2015.commit_parents
JOIN public_commits ON commit_parents.commit_id = public_commits.id;

CREATE VIEW public_forks AS
SELECT forks.*
FROM ghtorrent_restore_2015.forks
JOIN public_projects ON forks.forked_project_id = public_projects.id;

CREATE VIEW public_issues AS
SELECT issues.*
FROM ghtorrent_restore_2015.issues
JOIN public_projects ON issues.repo_id = public_projects.id;

CREATE VIEW public_pull_requests AS
SELECT pull_requests.*
FROM ghtorrent_restore_2015.pull_requests
JOIN public_projects ON pull_requests.base_repo_id = public_projects.id;

CREATE VIEW public_watchers AS
SELECT watchers.*
FROM ghtorrent_restore_2015.watchers
JOIN public_projects ON watchers.repo_id = public_projects.id;


CREATE VIEW public_pull_request_commits AS
SELECT pull_request_commits.*
FROM ghtorrent_restore_2015.pull_request_commits
JOIN public_commits ON pull_request_commits.commit_id = public_commits.id;

CREATE VIEW public_issue_comments AS
SELECT issue_comments.*
FROM ghtorrent_restore_2015.issue_comments
JOIN public_issues ON issue_comments.issue_id = public_issues.id;

CREATE VIEW public_issue_events AS
SELECT issue_events.*
FROM ghtorrent_restore_2015.issue_events
JOIN public_issues ON issue_events.issue_id = public_issues.id;

CREATE VIEW public_issue_labels AS
SELECT issue_labels.*
FROM ghtorrent_restore_2015.issue_labels
JOIN public_issues ON issue_labels.issue_id = public_issues.id;

CREATE VIEW public_issue_metrics AS
SELECT issue_metrics.*
FROM ghtorrent_restore_2015.issue_metrics
JOIN public_issues ON issue_metrics.issue_id = public_issues.id;

CREATE VIEW public_pull_request_comments AS
SELECT pull_request_comments.*
FROM ghtorrent_restore_2015.pull_request_comments
JOIN public_pull_requests ON pull_request_comments.pull_request_id = public_pull_requests.id;

CREATE VIEW public_pull_request_history AS
SELECT pull_request_history.*
FROM ghtorrent_restore_2015.pull_request_history
JOIN public_pull_requests ON pull_request_history.pull_request_id = public_pull_requests.id;

CREATE VIEW public_pull_request_metrics AS
SELECT pull_request_metrics.*
FROM ghtorrent_restore_2015.pull_request_metrics
JOIN public_pull_requests ON pull_request_metrics.pull_request_id = public_pull_requests.id;

-- CREATE VIEW public_followers AS
-- SELECT followers.*
-- FROM ghtorrent_restore_2015.followers
-- JOIN ghtorrent_restore_2015.users ON followers.public_id = users.id;

-- CREATE VIEW public_organization_members AS
-- SELECT organization_members.*
-- FROM ghtorrent_restore_2015.organization_members
-- JOIN ghtorrent_restore_2015.users ON organization_members.public_id = users.id;

-- CREATE VIEW public_metrics AS
-- SELECT public_metrics.*
-- FROM ghtorrent_restore_2015.public_metrics
-- JOIN ghtorrent_restore_2015.extractions ON public_metrics.extraction_id = extractions.id
-- JOIN ghtorrent_restore_2015.users ON extractions.user_id = users.id;

CREATE VIEW public_repo_labels AS
SELECT repo_labels.*
FROM ghtorrent_restore_2015.repo_labels
JOIN public_projects ON repo_labels.repo_id = public_projects.id;

CREATE VIEW public_repo_milestones AS
SELECT repo_milestones.*
FROM ghtorrent_restore_2015.repo_milestones
JOIN public_projects ON repo_milestones.repo_id = public_projects.id;