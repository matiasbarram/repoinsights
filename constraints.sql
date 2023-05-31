\connect ghtorrent_restore_2015


-- CREATE UNIQUE INDEX idx_16393_comment_id ON ghtorrent_restore_2015.commit_comments USING btree (comment_id);

CREATE INDEX idx_16393_commit_id ON ghtorrent_restore_2015.commit_comments USING btree (commit_id);

CREATE INDEX idx_16393_user_id ON ghtorrent_restore_2015.commit_comments USING btree (user_id);

CREATE INDEX idx_16399_parent_id ON ghtorrent_restore_2015.commit_parents USING btree (parent_id);


CREATE INDEX idx_16403_author_id ON ghtorrent_restore_2015.commits USING btree (author_id);



CREATE INDEX idx_16403_committer_id ON ghtorrent_restore_2015.commits USING btree (committer_id);
 
CREATE INDEX idx_16403_project_id ON ghtorrent_restore_2015.commits USING btree (project_id);


  
CREATE UNIQUE INDEX idx_16403_sha ON ghtorrent_restore_2015.commits USING btree (sha);


  
CREATE INDEX idx_16409_follower_id ON ghtorrent_restore_2015.followers USING btree (follower_id);


  
CREATE UNIQUE INDEX idx_16414_fork_id ON ghtorrent_restore_2015.forks USING btree (fork_id);


  
CREATE INDEX idx_16414_forked_from_id ON ghtorrent_restore_2015.forks USING btree (forked_from_id);


  
CREATE INDEX idx_16419_issue_id ON ghtorrent_restore_2015.issue_comments USING btree (issue_id);


  
CREATE INDEX idx_16419_user_id ON ghtorrent_restore_2015.issue_comments USING btree (user_id);


  
CREATE INDEX idx_16426_actor_id ON ghtorrent_restore_2015.issue_events USING btree (actor_id);


  
CREATE INDEX idx_16426_issue_id ON ghtorrent_restore_2015.issue_events USING btree (issue_id);

  CREATE INDEX idx_16426_extraction_id ON ghtorrent_restore_2015.extractions USING btree (project_id);



  
CREATE INDEX idx_16433_label_id ON ghtorrent_restore_2015.issue_labels USING btree (label_id);


  
CREATE INDEX idx_16439_assignee_id ON ghtorrent_restore_2015.issues USING btree (assignee_id);


  
CREATE INDEX idx_16439_pull_request_id ON ghtorrent_restore_2015.issues USING btree (pull_request_id);


  
CREATE INDEX idx_16439_repo_id ON ghtorrent_restore_2015.issues USING btree (repo_id);


  
CREATE INDEX idx_16439_reporter_id ON ghtorrent_restore_2015.issues USING btree (reporter_id);


  
CREATE INDEX idx_16447_user_id ON ghtorrent_restore_2015.organization_members USING btree (user_id);


  
CREATE INDEX idx_16451_commit_id ON ghtorrent_restore_2015.project_commits USING btree (commit_id);


  
CREATE INDEX idx_16456_user_id ON ghtorrent_restore_2015.project_members USING btree (user_id);


  
CREATE INDEX idx_16462_forked_from ON ghtorrent_restore_2015.projects USING btree (forked_from);


  
CREATE UNIQUE INDEX idx_16462_name ON ghtorrent_restore_2015.projects USING btree (name, owner_id);


  
CREATE INDEX idx_16462_owner_id ON ghtorrent_restore_2015.projects USING btree (owner_id);


  
CREATE INDEX idx_16471_commit_id ON ghtorrent_restore_2015.pull_request_comments USING btree (commit_id);


  
CREATE INDEX idx_16471_pull_request_id ON ghtorrent_restore_2015.pull_request_comments USING btree (pull_request_id);


  
CREATE INDEX idx_16471_user_id ON ghtorrent_restore_2015.pull_request_comments USING btree (user_id);


  
CREATE INDEX idx_16478_commit_id ON ghtorrent_restore_2015.pull_request_commits USING btree (commit_id);


  
CREATE INDEX idx_16482_actor_id ON ghtorrent_restore_2015.pull_request_history USING btree (actor_id);


  
CREATE INDEX idx_16482_pull_request_id ON ghtorrent_restore_2015.pull_request_history USING btree (pull_request_id);


  
CREATE INDEX idx_16489_base_commit_id ON ghtorrent_restore_2015.pull_requests USING btree (base_commit_id);


  
CREATE INDEX idx_16489_base_repo_id ON ghtorrent_restore_2015.pull_requests USING btree (base_repo_id);


  
CREATE INDEX idx_16489_head_commit_id ON ghtorrent_restore_2015.pull_requests USING btree (head_commit_id);


  
CREATE INDEX idx_16489_head_repo_id ON ghtorrent_restore_2015.pull_requests USING btree (head_repo_id);


  
CREATE UNIQUE INDEX idx_16489_pullreq_id ON ghtorrent_restore_2015.pull_requests USING btree (pullreq_id, base_repo_id);


  
CREATE INDEX idx_16489_user_id ON ghtorrent_restore_2015.pull_requests USING btree (user_id);


  
CREATE INDEX idx_16495_repo_id ON ghtorrent_restore_2015.repo_labels USING btree (repo_id);


  
CREATE INDEX idx_16501_repo_id ON ghtorrent_restore_2015.repo_milestones USING btree (repo_id);


  
CREATE UNIQUE INDEX idx_16511_login ON ghtorrent_restore_2015.users USING btree (login);


  
CREATE INDEX idx_16520_user_id ON ghtorrent_restore_2015.watchers USING btree (user_id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.commit_comments
    ADD CONSTRAINT commit_comments_ibfk_1 FOREIGN KEY (commit_id) REFERENCES ghtorrent_restore_2015.commits(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.commit_comments
    ADD CONSTRAINT commit_comments_ibfk_2 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.commit_parents
    ADD CONSTRAINT commit_parents_ibfk_1 FOREIGN KEY (commit_id) REFERENCES ghtorrent_restore_2015.commits(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.commit_parents
    ADD CONSTRAINT commit_parents_ibfk_2 FOREIGN KEY (parent_id) REFERENCES ghtorrent_restore_2015.commits(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.commits
    ADD CONSTRAINT commits_ibfk_1 FOREIGN KEY (author_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.commits
    ADD CONSTRAINT commits_ibfk_2 FOREIGN KEY (committer_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.commits
    ADD CONSTRAINT commits_ibfk_3 FOREIGN KEY (project_id) REFERENCES ghtorrent_restore_2015.projects(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.followers
    ADD CONSTRAINT followers_ibfk_1 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.followers
    ADD CONSTRAINT followers_ibfk_2 FOREIGN KEY (follower_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.forks
    ADD CONSTRAINT forks_ibfk_1 FOREIGN KEY (forked_project_id) REFERENCES ghtorrent_restore_2015.projects(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.forks
    ADD CONSTRAINT forks_ibfk_2 FOREIGN KEY (forked_from_id) REFERENCES ghtorrent_restore_2015.projects(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.issue_comments
    ADD CONSTRAINT issue_comments_ibfk_2 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.issue_events
    ADD CONSTRAINT issue_events_ibfk_2 FOREIGN KEY (actor_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.issue_labels
    ADD CONSTRAINT issue_labels_ibfk_1 FOREIGN KEY (label_id) REFERENCES ghtorrent_restore_2015.repo_labels(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.issues
    ADD CONSTRAINT issues_ibfk_1 FOREIGN KEY (repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.issues
    ADD CONSTRAINT issues_ibfk_2 FOREIGN KEY (reporter_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.issues
    ADD CONSTRAINT issues_ibfk_3 FOREIGN KEY (assignee_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.issues
    ADD CONSTRAINT issues_ibfk_4 FOREIGN KEY (pull_request_id) REFERENCES ghtorrent_restore_2015.pull_requests(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.organization_members
    ADD CONSTRAINT organization_members_ibfk_1 FOREIGN KEY (org_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.organization_members
    ADD CONSTRAINT organization_members_ibfk_2 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.project_commits
    ADD CONSTRAINT project_commits_ibfk_1 FOREIGN KEY (project_id) REFERENCES ghtorrent_restore_2015.projects(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.project_commits
    ADD CONSTRAINT project_commits_ibfk_2 FOREIGN KEY (commit_id) REFERENCES ghtorrent_restore_2015.commits(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.project_members
    ADD CONSTRAINT project_members_ibfk_1 FOREIGN KEY (repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.project_members
    ADD CONSTRAINT project_members_ibfk_2 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.projects
    ADD CONSTRAINT projects_ibfk_1 FOREIGN KEY (owner_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.projects
    ADD CONSTRAINT projects_ibfk_2 FOREIGN KEY (forked_from) REFERENCES ghtorrent_restore_2015.projects(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_comments
    ADD CONSTRAINT pull_request_comments_ibfk_1 FOREIGN KEY (pull_request_id) REFERENCES ghtorrent_restore_2015.pull_requests(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_comments
    ADD CONSTRAINT pull_request_comments_ibfk_2 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_comments
    ADD CONSTRAINT pull_request_comments_ibfk_3 FOREIGN KEY (commit_id) REFERENCES ghtorrent_restore_2015.commits(id);

  ALTER TABLE ONLY ghtorrent_restore_2015.extractions
    ADD CONSTRAINT extraction_metadata_ibfk_1 FOREIGN KEY (project_id) REFERENCES ghtorrent_restore_2015.projects(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_commits
    ADD CONSTRAINT pull_request_commits_ibfk_1 FOREIGN KEY (pull_request_id) REFERENCES ghtorrent_restore_2015.pull_requests(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_commits
    ADD CONSTRAINT pull_request_commits_ibfk_2 FOREIGN KEY (commit_id) REFERENCES ghtorrent_restore_2015.commits(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_history
    ADD CONSTRAINT pull_request_history_ibfk_1 FOREIGN KEY (pull_request_id) REFERENCES ghtorrent_restore_2015.pull_requests(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_history
    ADD CONSTRAINT pull_request_history_ibfk_2 FOREIGN KEY (actor_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests
    ADD CONSTRAINT pull_requests_ibfk_1 FOREIGN KEY (head_repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests
    ADD CONSTRAINT pull_requests_ibfk_2 FOREIGN KEY (base_repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests
    ADD CONSTRAINT pull_requests_ibfk_3 FOREIGN KEY (head_commit_id) REFERENCES ghtorrent_restore_2015.commits(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests
    ADD CONSTRAINT pull_requests_ibfk_4 FOREIGN KEY (base_commit_id) REFERENCES ghtorrent_restore_2015.commits(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests
    ADD CONSTRAINT pull_requests_ibfk_5 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.repo_labels
    ADD CONSTRAINT repo_labels_ibfk_1 FOREIGN KEY (repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.repo_milestones
    ADD CONSTRAINT repo_milestones_ibfk_1 FOREIGN KEY (repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.watchers
    ADD CONSTRAINT watchers_ibfk_1 FOREIGN KEY (repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


  
ALTER TABLE ONLY ghtorrent_restore_2015.watchers
    ADD CONSTRAINT watchers_ibfk_2 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


  
  
  

ALTER TABLE ONLY ghtorrent_restore_2015.project_metrics
    ADD CONSTRAINT project_metrics_ibfk_1 FOREIGN KEY (extraction_id) REFERENCES ghtorrent_restore_2015.extractions(id);

ALTER TABLE ONLY ghtorrent_restore_2015.project_metrics
    ADD CONSTRAINT project_metrics_ibfk_2 FOREIGN KEY (metric_id) REFERENCES ghtorrent_restore_2015.metrics(id);





ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_metrics    
    ADD CONSTRAINT pull_request_metrics_ibfk_1 FOREIGN KEY (extraction_id) REFERENCES ghtorrent_restore_2015.extractions(id);

ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_metrics    
    ADD CONSTRAINT pull_request_metrics_ibfk_2 FOREIGN KEY (pull_request_id) REFERENCES ghtorrent_restore_2015.pull_requests(id);

ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_metrics    
    ADD CONSTRAINT pull_request_metrics_ibfk_3 FOREIGN KEY (metric_id) REFERENCES ghtorrent_restore_2015.metrics(id);


ALTER TABLE ONLY ghtorrent_restore_2015.issue_metrics    
    ADD CONSTRAINT issue_metrics_ibfk_1 FOREIGN KEY (extraction_id) REFERENCES ghtorrent_restore_2015.extractions(id);

ALTER TABLE ONLY ghtorrent_restore_2015.issue_metrics
    ADD CONSTRAINT issue_metrics_ibfk_2 FOREIGN KEY (issue_id) REFERENCES ghtorrent_restore_2015.issues(id);

ALTER TABLE ONLY ghtorrent_restore_2015.issue_metrics
    ADD CONSTRAINT issue_metrics_ibfk_3 FOREIGN KEY (metric_id) REFERENCES ghtorrent_restore_2015.metrics(id);


ALTER TABLE ONLY ghtorrent_restore_2015.user_metrics
    ADD CONSTRAINT user_metrics_ibfk_3 FOREIGN KEY (extraction_id) REFERENCES ghtorrent_restore_2015.extractions(id);

ALTER TABLE ONLY ghtorrent_restore_2015.user_metrics
    ADD CONSTRAINT user_metrics_ibfk_1 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);

ALTER TABLE ONLY ghtorrent_restore_2015.user_metrics
    ADD CONSTRAINT user_metrics_ibfk_2 FOREIGN KEY (metric_id) REFERENCES ghtorrent_restore_2015.metrics(id);



  CREATE ROLE readonly_user WITH LOGIN PASSWORD 'readonly_user_password';

  GRANT USAGE ON SCHEMA ghtorrent_restore_2015 TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA ghtorrent_restore_2015 TO readonly_user;

  GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;


SELECT setval('ghtorrent_restore_2015.commit_comments_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.commit_comments));

SELECT setval('ghtorrent_restore_2015.commits_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.commits));

SELECT setval('ghtorrent_restore_2015.issues_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.issues));

SELECT setval('ghtorrent_restore_2015.projects_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.projects));

SELECT setval('ghtorrent_restore_2015.pull_request_history_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.pull_request_history));

SELECT setval('ghtorrent_restore_2015.pull_requests_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.pull_requests));

SELECT setval('ghtorrent_restore_2015.repo_labels_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.repo_labels));

SELECT setval('ghtorrent_restore_2015.repo_milestones_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.repo_milestones));

SELECT setval('ghtorrent_restore_2015.users_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.users));

SELECT setval('ghtorrent_restore_2015.extractions_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.extractions));

SELECT setval('ghtorrent_restore_2015.pull_request_comments_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.pull_request_comments));

SELECT setval('ghtorrent_restore_2015.issue_comments_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.issue_comments));

SELECT setval('ghtorrent_restore_2015.project_metrics_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.project_metrics));

SELECT setval('ghtorrent_restore_2015.pull_request_metrics_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.pull_request_metrics));

SELECT setval('ghtorrent_restore_2015.issue_metrics_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.issue_metrics));

SELECT setval('ghtorrent_restore_2015.user_metrics_id_seq', (SELECT MAX(id) FROM ghtorrent_restore_2015.user_metrics));