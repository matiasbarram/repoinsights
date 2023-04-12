SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
CREATE SCHEMA ghtorrent_restore_2015;
ALTER SCHEMA ghtorrent_restore_2015 OWNER TO ghtorrent;

SET default_tablespace = '';

SET default_table_access_method = heap;
CREATE TABLE ghtorrent_restore_2015.commit_comments (
    id integer NOT NULL,
    commit_id integer NOT NULL,
    user_id integer NOT NULL,
    body character varying(256),
    line integer,
    "position" integer,
    comment_id integer NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.commit_comments OWNER TO ghtorrent;
CREATE SEQUENCE ghtorrent_restore_2015.commit_comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ghtorrent_restore_2015.commit_comments_id_seq OWNER TO ghtorrent;
ALTER SEQUENCE ghtorrent_restore_2015.commit_comments_id_seq OWNED BY ghtorrent_restore_2015.commit_comments.id;
CREATE TABLE ghtorrent_restore_2015.commit_parents (
    commit_id integer NOT NULL,
    parent_id integer NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.commit_parents OWNER TO ghtorrent;
CREATE TABLE ghtorrent_restore_2015.commits (
    id integer NOT NULL,
    sha character varying(40),
    author_id integer,
    committer_id integer,
    project_id integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.commits OWNER TO ghtorrent;
CREATE SEQUENCE ghtorrent_restore_2015.commits_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ghtorrent_restore_2015.commits_id_seq OWNER TO ghtorrent;
ALTER SEQUENCE ghtorrent_restore_2015.commits_id_seq OWNED BY ghtorrent_restore_2015.commits.id;
CREATE TABLE ghtorrent_restore_2015.followers (
    user_id integer NOT NULL,
    follower_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.followers OWNER TO ghtorrent;
CREATE TABLE ghtorrent_restore_2015.forks (
    forked_project_id integer NOT NULL,
    forked_from_id integer NOT NULL,
    fork_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.forks OWNER TO ghtorrent;
CREATE TABLE ghtorrent_restore_2015.issue_comments (
    issue_id integer NOT NULL,
    user_id integer NOT NULL,
    comment_id text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.issue_comments OWNER TO ghtorrent;
CREATE TABLE ghtorrent_restore_2015.issue_events (
    event_id text NOT NULL,
    issue_id integer NOT NULL,
    actor_id integer NOT NULL,
    action character varying(255) NOT NULL,
    action_specific character varying(50),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.issue_events OWNER TO ghtorrent;
CREATE TABLE ghtorrent_restore_2015.issue_labels (
    label_id integer DEFAULT 0 NOT NULL,
    issue_id integer DEFAULT 0 NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.issue_labels OWNER TO ghtorrent;
CREATE TABLE ghtorrent_restore_2015.issues (
    id integer NOT NULL,
    repo_id integer,
    reporter_id integer,
    assignee_id integer,
    issue_id text NOT NULL,
    pull_request boolean NOT NULL,
    pull_request_id integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.issues OWNER TO ghtorrent;
CREATE SEQUENCE ghtorrent_restore_2015.issues_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ghtorrent_restore_2015.issues_id_seq OWNER TO ghtorrent;
ALTER SEQUENCE ghtorrent_restore_2015.issues_id_seq OWNED BY ghtorrent_restore_2015.issues.id;
CREATE TABLE ghtorrent_restore_2015.organization_members (
    org_id integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.organization_members OWNER TO ghtorrent;
CREATE TABLE ghtorrent_restore_2015.project_commits (
    project_id integer DEFAULT 0 NOT NULL,
    commit_id integer DEFAULT 0 NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.project_commits OWNER TO ghtorrent;
CREATE TABLE ghtorrent_restore_2015.project_members (
    repo_id integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.project_members OWNER TO ghtorrent;
CREATE TABLE ghtorrent_restore_2015.projects (
    id integer NOT NULL,
    url character varying(255),
    owner_id integer,
    name character varying(255) NOT NULL,
    description character varying(255),
    language character varying(255),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL,
    forked_from integer,
    deleted boolean DEFAULT false NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.projects OWNER TO ghtorrent;
CREATE SEQUENCE ghtorrent_restore_2015.projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ghtorrent_restore_2015.projects_id_seq OWNER TO ghtorrent;
ALTER SEQUENCE ghtorrent_restore_2015.projects_id_seq OWNED BY ghtorrent_restore_2015.projects.id;
CREATE TABLE ghtorrent_restore_2015.pull_request_comments (
    pull_request_id integer NOT NULL,
    user_id integer NOT NULL,
    comment_id text NOT NULL,
    "position" integer,
    body character varying(256),
    commit_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.pull_request_comments OWNER TO ghtorrent;
CREATE TABLE ghtorrent_restore_2015.pull_request_commits (
    pull_request_id integer NOT NULL,
    commit_id integer NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.pull_request_commits OWNER TO ghtorrent;
CREATE TABLE ghtorrent_restore_2015.pull_request_history (
    id integer NOT NULL,
    pull_request_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL,
    action character varying(255) NOT NULL,
    actor_id integer
);
ALTER TABLE ghtorrent_restore_2015.pull_request_history OWNER TO ghtorrent;
CREATE SEQUENCE ghtorrent_restore_2015.pull_request_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ghtorrent_restore_2015.pull_request_history_id_seq OWNER TO ghtorrent;
ALTER SEQUENCE ghtorrent_restore_2015.pull_request_history_id_seq OWNED BY ghtorrent_restore_2015.pull_request_history.id;
CREATE TABLE ghtorrent_restore_2015.pull_requests (
    id integer NOT NULL,
    head_repo_id integer,
    base_repo_id integer NOT NULL,
    head_commit_id integer,
    base_commit_id integer NOT NULL,
    user_id integer NOT NULL,
    pullreq_id integer NOT NULL,
    intra_branch boolean NOT NULL,
    merged boolean DEFAULT false NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.pull_requests OWNER TO ghtorrent;
CREATE SEQUENCE ghtorrent_restore_2015.pull_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ghtorrent_restore_2015.pull_requests_id_seq OWNER TO ghtorrent;
ALTER SEQUENCE ghtorrent_restore_2015.pull_requests_id_seq OWNED BY ghtorrent_restore_2015.pull_requests.id;
CREATE TABLE ghtorrent_restore_2015.repo_labels (
    id integer NOT NULL,
    repo_id integer,
    name character varying(24) NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.repo_labels OWNER TO ghtorrent;
CREATE SEQUENCE ghtorrent_restore_2015.repo_labels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ghtorrent_restore_2015.repo_labels_id_seq OWNER TO ghtorrent;
ALTER SEQUENCE ghtorrent_restore_2015.repo_labels_id_seq OWNED BY ghtorrent_restore_2015.repo_labels.id;
CREATE TABLE ghtorrent_restore_2015.repo_milestones (
    id integer NOT NULL,
    repo_id integer,
    name character varying(24) NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.repo_milestones OWNER TO ghtorrent;
CREATE SEQUENCE ghtorrent_restore_2015.repo_milestones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ghtorrent_restore_2015.repo_milestones_id_seq OWNER TO ghtorrent;
ALTER SEQUENCE ghtorrent_restore_2015.repo_milestones_id_seq OWNED BY ghtorrent_restore_2015.repo_milestones.id;
CREATE TABLE ghtorrent_restore_2015.schema_info (
    version integer DEFAULT 0 NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.schema_info OWNER TO ghtorrent;
CREATE TABLE ghtorrent_restore_2015.users (
    id integer NOT NULL,
    login character varying(255) NOT NULL,
    name character varying(255),
    company character varying(255),
    location character varying(255),
    email character varying(255),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL,
    type character varying(255) DEFAULT 'USR'::character varying NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.users OWNER TO ghtorrent;
CREATE SEQUENCE ghtorrent_restore_2015.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ghtorrent_restore_2015.users_id_seq OWNER TO ghtorrent;
ALTER SEQUENCE ghtorrent_restore_2015.users_id_seq OWNED BY ghtorrent_restore_2015.users.id;
CREATE TABLE ghtorrent_restore_2015.watchers (
    repo_id integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(24) DEFAULT '0'::character varying NOT NULL
);
ALTER TABLE ghtorrent_restore_2015.watchers OWNER TO ghtorrent;
ALTER TABLE ONLY ghtorrent_restore_2015.commit_comments ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.commit_comments_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.commits ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.commits_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.issues ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.issues_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.projects ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.projects_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_history ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.pull_request_history_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.pull_requests_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.repo_labels ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.repo_labels_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.repo_milestones ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.repo_milestones_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.users ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.users_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.commit_comments
    ADD CONSTRAINT idx_16393_primary PRIMARY KEY (id);
ALTER TABLE ONLY ghtorrent_restore_2015.commit_parents
    ADD CONSTRAINT idx_16399_primary PRIMARY KEY (commit_id, parent_id);
ALTER TABLE ONLY ghtorrent_restore_2015.commits
    ADD CONSTRAINT idx_16403_primary PRIMARY KEY (id);
ALTER TABLE ONLY ghtorrent_restore_2015.followers
    ADD CONSTRAINT idx_16409_primary PRIMARY KEY (user_id, follower_id);
ALTER TABLE ONLY ghtorrent_restore_2015.forks
    ADD CONSTRAINT idx_16414_primary PRIMARY KEY (forked_project_id, forked_from_id);
ALTER TABLE ONLY ghtorrent_restore_2015.issue_labels
    ADD CONSTRAINT idx_16433_primary PRIMARY KEY (issue_id, label_id);
ALTER TABLE ONLY ghtorrent_restore_2015.issues
    ADD CONSTRAINT idx_16439_primary PRIMARY KEY (id);
ALTER TABLE ONLY ghtorrent_restore_2015.organization_members
    ADD CONSTRAINT idx_16447_primary PRIMARY KEY (org_id, user_id);
ALTER TABLE ONLY ghtorrent_restore_2015.project_commits
    ADD CONSTRAINT idx_16451_primary PRIMARY KEY (project_id, commit_id);
ALTER TABLE ONLY ghtorrent_restore_2015.project_members
    ADD CONSTRAINT idx_16456_primary PRIMARY KEY (repo_id, user_id);
ALTER TABLE ONLY ghtorrent_restore_2015.projects
    ADD CONSTRAINT idx_16462_primary PRIMARY KEY (id);
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_commits
    ADD CONSTRAINT idx_16478_primary PRIMARY KEY (pull_request_id, commit_id);
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_history
    ADD CONSTRAINT idx_16482_primary PRIMARY KEY (id);
ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests
    ADD CONSTRAINT idx_16489_primary PRIMARY KEY (id);
ALTER TABLE ONLY ghtorrent_restore_2015.repo_labels
    ADD CONSTRAINT idx_16495_primary PRIMARY KEY (id);
ALTER TABLE ONLY ghtorrent_restore_2015.repo_milestones
    ADD CONSTRAINT idx_16501_primary PRIMARY KEY (id);
ALTER TABLE ONLY ghtorrent_restore_2015.users
    ADD CONSTRAINT idx_16511_primary PRIMARY KEY (id);
ALTER TABLE ONLY ghtorrent_restore_2015.watchers
    ADD CONSTRAINT idx_16520_primary PRIMARY KEY (repo_id, user_id);
CREATE UNIQUE INDEX idx_16393_comment_id ON ghtorrent_restore_2015.commit_comments USING btree (comment_id);
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
