--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2 (Debian 15.2-1.pgdg110+1)
-- Dumped by pg_dump version 15.2

-- Started on 2023-04-12 17:20:53

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

--
-- TOC entry 3584 (class 1262 OID 16390)
-- Name: ghtorrent_restore_2015; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE ghtorrent_restore_2015 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


\connect ghtorrent_restore_2015

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

--
-- TOC entry 3585 (class 0 OID 0)
-- Name: ghtorrent_restore_2015; Type: DATABASE PROPERTIES; Schema: -; Owner: -
--

ALTER DATABASE ghtorrent_restore_2015 SET search_path TO 'public', 'ghtorrent_restore_2015';


\connect ghtorrent_restore_2015

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

--
-- TOC entry 6 (class 2615 OID 16391)
-- Name: ghtorrent_restore_2015; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA ghtorrent_restore_2015;


SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 16393)
-- Name: commit_comments; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.commit_comments (
    id integer NOT NULL,
    commit_id integer NOT NULL,
    user_id integer NOT NULL,
    body character varying(256),
    line integer,
    "position" integer,
    comment_id integer NOT NULL,
    ext_ref_id character varying(32) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- TOC entry 217 (class 1259 OID 16392)
-- Name: commit_comments_id_seq; Type: SEQUENCE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE SEQUENCE ghtorrent_restore_2015.commit_comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3586 (class 0 OID 0)
-- Dependencies: 217
-- Name: commit_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER SEQUENCE ghtorrent_restore_2015.commit_comments_id_seq OWNED BY ghtorrent_restore_2015.commit_comments.id;


--
-- TOC entry 219 (class 1259 OID 16399)
-- Name: commit_parents; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.commit_parents (
    commit_id integer NOT NULL,
    parent_id integer NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 221 (class 1259 OID 16403)
-- Name: commits; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.commits (
    id integer NOT NULL,
    sha character varying(40),
    author_id integer,
    committer_id integer,
    project_id integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    message character varying(256),
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 220 (class 1259 OID 16402)
-- Name: commits_id_seq; Type: SEQUENCE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE SEQUENCE ghtorrent_restore_2015.commits_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3587 (class 0 OID 0)
-- Dependencies: 220
-- Name: commits_id_seq; Type: SEQUENCE OWNED BY; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER SEQUENCE ghtorrent_restore_2015.commits_id_seq OWNED BY ghtorrent_restore_2015.commits.id;


--
-- TOC entry 222 (class 1259 OID 16409)
-- Name: followers; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.followers (
    user_id integer NOT NULL,
    follower_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 223 (class 1259 OID 16414)
-- Name: forks; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.forks (
    forked_project_id integer NOT NULL,
    forked_from_id integer NOT NULL,
    fork_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 224 (class 1259 OID 16419)
-- Name: issue_comments; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.issue_comments (
    id integer NOT NULL,
    issue_id integer NOT NULL,
    user_id integer NOT NULL,
    comment_id text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);

CREATE SEQUENCE ghtorrent_restore_2015.issue_comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE ghtorrent_restore_2015.issue_comments_id_seq OWNED BY ghtorrent_restore_2015.issue_comments.id;

--
-- TOC entry 225 (class 1259 OID 16426)
-- Name: issue_events; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.issue_events (
    event_id text NOT NULL,
    issue_id integer NOT NULL,
    actor_id integer,
    action character varying(255) NOT NULL,
    action_specific character varying(50),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 226 (class 1259 OID 16433)
-- Name: issue_labels; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.issue_labels (
    label_id integer DEFAULT 0 NOT NULL,
    issue_id integer DEFAULT 0 NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 228 (class 1259 OID 16439)
-- Name: issues; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.issues (
    id integer NOT NULL,
    repo_id integer,
    reporter_id integer,
    assignee_id integer,
    issue_id text NOT NULL,
    pull_request boolean NOT NULL,
    pull_request_id integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 227 (class 1259 OID 16438)
-- Name: issues_id_seq; Type: SEQUENCE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE SEQUENCE ghtorrent_restore_2015.issues_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3588 (class 0 OID 0)
-- Dependencies: 227
-- Name: issues_id_seq; Type: SEQUENCE OWNED BY; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER SEQUENCE ghtorrent_restore_2015.issues_id_seq OWNED BY ghtorrent_restore_2015.issues.id;


--
-- TOC entry 229 (class 1259 OID 16447)
-- Name: organization_members; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.organization_members (
    org_id integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 230 (class 1259 OID 16451)
-- Name: project_commits; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.project_commits (
    project_id integer DEFAULT 0 NOT NULL,
    commit_id integer DEFAULT 0 NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 231 (class 1259 OID 16456)
-- Name: project_members; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.project_members (
    repo_id integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 233 (class 1259 OID 16462)
-- Name: projects; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.projects (
    id integer NOT NULL,
    url character varying(255),
    owner_id integer,
    name character varying(255) NOT NULL,
    description character varying(255),
    language character varying(255),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) NOT NULL,
    forked_from integer,
    deleted boolean DEFAULT false NOT NULL,
    private boolean DEFAULT false NOT NULL
    /*last_extraction timestamp with time zone DEFAULT CURRENT_TIMESTAMP*/
);


--
-- TOC entry 232 (class 1259 OID 16461)
-- Name: projects_id_seq; Type: SEQUENCE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE SEQUENCE ghtorrent_restore_2015.projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3589 (class 0 OID 0)
-- Dependencies: 232
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER SEQUENCE ghtorrent_restore_2015.projects_id_seq OWNED BY ghtorrent_restore_2015.projects.id;



CREATE TABLE ghtorrent_restore_2015.extractions (
    id integer NOT NULL,
    project_id integer NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ext_ref_id character varying(32) NOT NULL
);

CREATE SEQUENCE ghtorrent_restore_2015.extractions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE ghtorrent_restore_2015.extractions_id_seq OWNED BY ghtorrent_restore_2015.extractions.id;


--
-- TOC entry 234 (class 1259 OID 16471)
-- Name: pull_request_comments; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.pull_request_comments (
    id integer NOT NULL,
    pull_request_id integer NOT NULL,
    user_id integer,
    comment_id text NOT NULL,
    "position" integer,
    body character varying(256),
    commit_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);

CREATE SEQUENCE ghtorrent_restore_2015.pull_request_comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE ghtorrent_restore_2015.pull_request_comments_id_seq OWNED BY ghtorrent_restore_2015.pull_request_comments.id;


--
-- TOC entry 235 (class 1259 OID 16478)
-- Name: pull_request_commits; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.pull_request_commits (
    pull_request_id integer NOT NULL,
    commit_id integer NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 237 (class 1259 OID 16482)
-- Name: pull_request_history; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.pull_request_history (
    id integer NOT NULL,
    pull_request_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) NOT NULL,
    action character varying(255) NOT NULL,
    actor_id integer
);


--
-- TOC entry 236 (class 1259 OID 16481)
-- Name: pull_request_history_id_seq; Type: SEQUENCE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE SEQUENCE ghtorrent_restore_2015.pull_request_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3590 (class 0 OID 0)
-- Dependencies: 236
-- Name: pull_request_history_id_seq; Type: SEQUENCE OWNED BY; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER SEQUENCE ghtorrent_restore_2015.pull_request_history_id_seq OWNED BY ghtorrent_restore_2015.pull_request_history.id;


--
-- TOC entry 239 (class 1259 OID 16489)
-- Name: pull_requests; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.pull_requests (
    id integer NOT NULL,
    head_repo_id integer,
    base_repo_id integer NOT NULL,
    head_commit_id integer,
    base_commit_id integer NOT NULL,
    user_id integer NOT NULL,
    pullreq_id integer NOT NULL,
    intra_branch boolean NOT NULL,
    additions integer,
    deletions integer,
    changed_files integer,
    merged boolean DEFAULT false NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 238 (class 1259 OID 16488)
-- Name: pull_requests_id_seq; Type: SEQUENCE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE SEQUENCE ghtorrent_restore_2015.pull_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3591 (class 0 OID 0)
-- Dependencies: 238
-- Name: pull_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER SEQUENCE ghtorrent_restore_2015.pull_requests_id_seq OWNED BY ghtorrent_restore_2015.pull_requests.id;


--
-- TOC entry 241 (class 1259 OID 16495)
-- Name: repo_labels; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.repo_labels (
    id integer NOT NULL,
    repo_id integer NOT NULL,
    name character varying(24) NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 240 (class 1259 OID 16494)
-- Name: repo_labels_id_seq; Type: SEQUENCE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE SEQUENCE ghtorrent_restore_2015.repo_labels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3592 (class 0 OID 0)
-- Dependencies: 240
-- Name: repo_labels_id_seq; Type: SEQUENCE OWNED BY; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER SEQUENCE ghtorrent_restore_2015.repo_labels_id_seq OWNED BY ghtorrent_restore_2015.repo_labels.id;


--
-- TOC entry 243 (class 1259 OID 16501)
-- Name: repo_milestones; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.repo_milestones (
    id integer NOT NULL,
    repo_id integer,
    name character varying(24) NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


--
-- TOC entry 242 (class 1259 OID 16500)
-- Name: repo_milestones_id_seq; Type: SEQUENCE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE SEQUENCE ghtorrent_restore_2015.repo_milestones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3593 (class 0 OID 0)
-- Dependencies: 242
-- Name: repo_milestones_id_seq; Type: SEQUENCE OWNED BY; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER SEQUENCE ghtorrent_restore_2015.repo_milestones_id_seq OWNED BY ghtorrent_restore_2015.repo_milestones.id;


--
-- TOC entry 244 (class 1259 OID 16506)
-- Name: schema_info; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.schema_info (
    version integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 246 (class 1259 OID 16511)
-- Name: users; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.users (
    id integer NOT NULL,
    login character varying(255) NOT NULL,
    name character varying(255),
    company character varying(255),
    location character varying(255),
    email character varying(255),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) NOT NULL,
    type character varying(255) DEFAULT 'USR'::character varying NOT NULL
);


--
-- TOC entry 245 (class 1259 OID 16510)
-- Name: users_id_seq; Type: SEQUENCE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE SEQUENCE ghtorrent_restore_2015.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3594 (class 0 OID 0)
-- Dependencies: 245
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER SEQUENCE ghtorrent_restore_2015.users_id_seq OWNED BY ghtorrent_restore_2015.users.id;


--
-- TOC entry 247 (class 1259 OID 16520)
-- Name: watchers; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.watchers (
    repo_id integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) NOT NULL
);


-- CUSTOM

CREATE TABLE ghtorrent_restore_2015.metrics (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


CREATE SEQUENCE ghtorrent_restore_2015.metrics_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE ghtorrent_restore_2015.metrics_seq OWNED BY ghtorrent_restore_2015.metrics.id;


CREATE TABLE ghtorrent_restore_2015.metrics_log (
    id integer NOT NULL,
    repo_id integer,
    metric_id integer NOT NULL,
    value integer NOT NULL,
    date timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- CUSTOM

CREATE SEQUENCE ghtorrent_restore_2015.metrics_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE ghtorrent_restore_2015.metrics_log_id_seq OWNED BY ghtorrent_restore_2015.metrics_log.id;





--
-- TOC entry 3271 (class 2604 OID 16396)
-- Name: commit_comments id; Type: DEFAULT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.commit_comments ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.commit_comments_id_seq'::regclass);


--
-- TOC entry 3274 (class 2604 OID 16406)
-- Name: commits id; Type: DEFAULT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.commits ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.commits_id_seq'::regclass);


--
-- TOC entry 3287 (class 2604 OID 16442)
-- Name: issues id; Type: DEFAULT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.issues ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.issues_id_seq'::regclass);


--
-- TOC entry 3295 (class 2604 OID 16465)
-- Name: projects id; Type: DEFAULT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.projects ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.projects_id_seq'::regclass);


--
-- TOC entry 3301 (class 2604 OID 16485)
-- Name: pull_request_history id; Type: DEFAULT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_history ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.pull_request_history_id_seq'::regclass);


--
-- TOC entry 3304 (class 2604 OID 16492)
-- Name: pull_requests id; Type: DEFAULT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.pull_requests_id_seq'::regclass);


--
-- TOC entry 3306 (class 2604 OID 16498)
-- Name: repo_labels id; Type: DEFAULT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.repo_labels ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.repo_labels_id_seq'::regclass);


--
-- TOC entry 3308 (class 2604 OID 16504)
-- Name: repo_milestones id; Type: DEFAULT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.repo_milestones ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.repo_milestones_id_seq'::regclass);


--
-- TOC entry 3311 (class 2604 OID 16514)
-- Name: users id; Type: DEFAULT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.users ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.users_id_seq'::regclass);


-- CUSTOM

ALTER TABLE ONLY ghtorrent_restore_2015.extractions ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.extractions_id_seq'::regclass);

ALTER TABLE ONLY ghtorrent_restore_2015.extractions
    ADD CONSTRAINT idx_12393_primary PRIMARY KEY (id);


-- CUSTOM

ALTER TABLE ONLY ghtorrent_restore_2015.metrics ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.metrics_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.metrics
    ADD CONSTRAINT idx_12394_primary PRIMARY KEY (id);

ALTER TABLE ONLY ghtorrent_restore_2015.metrics_log ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.metrics_log_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.metrics_log
    ADD CONSTRAINT idx_12395_primary PRIMARY KEY (id);


-- pull_request_comments_id_seq
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_comments ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.pull_request_comments_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_comments
    ADD CONSTRAINT idx_12396_primary PRIMARY KEY (id);


ALTER TABLE ONLY ghtorrent_restore_2015.issue_comments ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.issue_comments_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.issue_comments
    ADD CONSTRAINT idx_12397_primary PRIMARY KEY (id);
--
-- TOC entry 3320 (class 2606 OID 16606)
-- Name: commit_comments idx_16393_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.commit_comments
    ADD CONSTRAINT idx_16393_primary PRIMARY KEY (id);


--
-- TOC entry 3324 (class 2606 OID 16591)
-- Name: commit_parents idx_16399_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.commit_parents
    ADD CONSTRAINT idx_16399_primary PRIMARY KEY (commit_id, parent_id);


--
-- TOC entry 3328 (class 2606 OID 16594)
-- Name: commits idx_16403_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.commits
    ADD CONSTRAINT idx_16403_primary PRIMARY KEY (id);


--
-- TOC entry 3333 (class 2606 OID 16592)
-- Name: followers idx_16409_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.followers
    ADD CONSTRAINT idx_16409_primary PRIMARY KEY (user_id, follower_id);


--
-- TOC entry 3337 (class 2606 OID 16604)
-- Name: forks idx_16414_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.forks
    ADD CONSTRAINT idx_16414_primary PRIMARY KEY (forked_project_id, forked_from_id);


--
-- TOC entry 3344 (class 2606 OID 16602)
-- Name: issue_labels idx_16433_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.issue_labels
    ADD CONSTRAINT idx_16433_primary PRIMARY KEY (issue_id, label_id);


--
-- TOC entry 3347 (class 2606 OID 16600)
-- Name: issues idx_16439_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.issues
    ADD CONSTRAINT idx_16439_primary PRIMARY KEY (id);


--
-- TOC entry 3352 (class 2606 OID 16599)
-- Name: organization_members idx_16447_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.organization_members
    ADD CONSTRAINT idx_16447_primary PRIMARY KEY (org_id, user_id);


--
-- TOC entry 3356 (class 2606 OID 16593)
-- Name: project_commits idx_16451_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.project_commits
    ADD CONSTRAINT idx_16451_primary PRIMARY KEY (project_id, commit_id);


--
-- TOC entry 3358 (class 2606 OID 16608)
-- Name: project_members idx_16456_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.project_members
    ADD CONSTRAINT idx_16456_primary PRIMARY KEY (repo_id, user_id);


--
-- TOC entry 3364 (class 2606 OID 16605)
-- Name: projects idx_16462_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.projects
    ADD CONSTRAINT idx_16462_primary PRIMARY KEY (id);


--
-- TOC entry 3370 (class 2606 OID 16596)
-- Name: pull_request_commits idx_16478_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_commits
    ADD CONSTRAINT idx_16478_primary PRIMARY KEY (pull_request_id, commit_id);


--
-- TOC entry 3373 (class 2606 OID 16598)
-- Name: pull_request_history idx_16482_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_history
    ADD CONSTRAINT idx_16482_primary PRIMARY KEY (id);


--
-- TOC entry 3380 (class 2606 OID 16601)
-- Name: pull_requests idx_16489_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests
    ADD CONSTRAINT idx_16489_primary PRIMARY KEY (id);


--
-- TOC entry 3384 (class 2606 OID 16603)
-- Name: repo_labels idx_16495_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.repo_labels
    ADD CONSTRAINT idx_16495_primary PRIMARY KEY (id);


--
-- TOC entry 3387 (class 2606 OID 16607)
-- Name: repo_milestones idx_16501_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.repo_milestones
    ADD CONSTRAINT idx_16501_primary PRIMARY KEY (id);


--
-- TOC entry 3391 (class 2606 OID 16595)
-- Name: users idx_16511_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.users
    ADD CONSTRAINT idx_16511_primary PRIMARY KEY (id);


--
-- TOC entry 3393 (class 2606 OID 16597)
-- Name: watchers idx_16520_primary; Type: CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.watchers
    ADD CONSTRAINT idx_16520_primary PRIMARY KEY (repo_id, user_id);


--
-- TOC entry 3317 (class 1259 OID 16579)
-- Name: idx_16393_comment_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE UNIQUE INDEX idx_16393_comment_id ON ghtorrent_restore_2015.commit_comments USING btree (comment_id);


--
-- TOC entry 3318 (class 1259 OID 16577)
-- Name: idx_16393_commit_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16393_commit_id ON ghtorrent_restore_2015.commit_comments USING btree (commit_id);


--
-- TOC entry 3321 (class 1259 OID 16576)
-- Name: idx_16393_user_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16393_user_id ON ghtorrent_restore_2015.commit_comments USING btree (user_id);


--
-- TOC entry 3322 (class 1259 OID 16526)
-- Name: idx_16399_parent_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16399_parent_id ON ghtorrent_restore_2015.commit_parents USING btree (parent_id);


--
-- TOC entry 3325 (class 1259 OID 16536)
-- Name: idx_16403_author_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16403_author_id ON ghtorrent_restore_2015.commits USING btree (author_id);


--
-- TOC entry 3326 (class 1259 OID 16540)
-- Name: idx_16403_committer_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16403_committer_id ON ghtorrent_restore_2015.commits USING btree (committer_id);


--
-- TOC entry 3329 (class 1259 OID 16537)
-- Name: idx_16403_project_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16403_project_id ON ghtorrent_restore_2015.commits USING btree (project_id);


--
-- TOC entry 3330 (class 1259 OID 16539)
-- Name: idx_16403_sha; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE UNIQUE INDEX idx_16403_sha ON ghtorrent_restore_2015.commits USING btree (sha);


--
-- TOC entry 3331 (class 1259 OID 16528)
-- Name: idx_16409_follower_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16409_follower_id ON ghtorrent_restore_2015.followers USING btree (follower_id);


--
-- TOC entry 3334 (class 1259 OID 16569)
-- Name: idx_16414_fork_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE UNIQUE INDEX idx_16414_fork_id ON ghtorrent_restore_2015.forks USING btree (fork_id);


--
-- TOC entry 3335 (class 1259 OID 16570)
-- Name: idx_16414_forked_from_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16414_forked_from_id ON ghtorrent_restore_2015.forks USING btree (forked_from_id);


--
-- TOC entry 3338 (class 1259 OID 16534)
-- Name: idx_16419_issue_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16419_issue_id ON ghtorrent_restore_2015.issue_comments USING btree (issue_id);


--
-- TOC entry 3339 (class 1259 OID 16535)
-- Name: idx_16419_user_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16419_user_id ON ghtorrent_restore_2015.issue_comments USING btree (user_id);


--
-- TOC entry 3340 (class 1259 OID 16532)
-- Name: idx_16426_actor_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16426_actor_id ON ghtorrent_restore_2015.issue_events USING btree (actor_id);


--
-- TOC entry 3341 (class 1259 OID 16533)
-- Name: idx_16426_issue_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16426_issue_id ON ghtorrent_restore_2015.issue_events USING btree (issue_id);

-- CUSTOM 
CREATE INDEX idx_16426_extraction_id ON ghtorrent_restore_2015.extractions USING btree (project_id);



--
-- TOC entry 3342 (class 1259 OID 16564)
-- Name: idx_16433_label_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16433_label_id ON ghtorrent_restore_2015.issue_labels USING btree (label_id);


--
-- TOC entry 3345 (class 1259 OID 16553)
-- Name: idx_16439_assignee_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16439_assignee_id ON ghtorrent_restore_2015.issues USING btree (assignee_id);


--
-- TOC entry 3348 (class 1259 OID 16554)
-- Name: idx_16439_pull_request_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16439_pull_request_id ON ghtorrent_restore_2015.issues USING btree (pull_request_id);


--
-- TOC entry 3349 (class 1259 OID 16555)
-- Name: idx_16439_repo_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16439_repo_id ON ghtorrent_restore_2015.issues USING btree (repo_id);


--
-- TOC entry 3350 (class 1259 OID 16552)
-- Name: idx_16439_reporter_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16439_reporter_id ON ghtorrent_restore_2015.issues USING btree (reporter_id);


--
-- TOC entry 3353 (class 1259 OID 16551)
-- Name: idx_16447_user_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16447_user_id ON ghtorrent_restore_2015.organization_members USING btree (user_id);


--
-- TOC entry 3354 (class 1259 OID 16530)
-- Name: idx_16451_commit_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16451_commit_id ON ghtorrent_restore_2015.project_commits USING btree (commit_id);


--
-- TOC entry 3359 (class 1259 OID 16582)
-- Name: idx_16456_user_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16456_user_id ON ghtorrent_restore_2015.project_members USING btree (user_id);


--
-- TOC entry 3360 (class 1259 OID 16572)
-- Name: idx_16462_forked_from; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16462_forked_from ON ghtorrent_restore_2015.projects USING btree (forked_from);


--
-- TOC entry 3361 (class 1259 OID 16571)
-- Name: idx_16462_name; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE UNIQUE INDEX idx_16462_name ON ghtorrent_restore_2015.projects USING btree (name, owner_id);


--
-- TOC entry 3362 (class 1259 OID 16574)
-- Name: idx_16462_owner_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16462_owner_id ON ghtorrent_restore_2015.projects USING btree (owner_id);


--
-- TOC entry 3365 (class 1259 OID 16585)
-- Name: idx_16471_commit_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16471_commit_id ON ghtorrent_restore_2015.pull_request_comments USING btree (commit_id);


--
-- TOC entry 3366 (class 1259 OID 16583)
-- Name: idx_16471_pull_request_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16471_pull_request_id ON ghtorrent_restore_2015.pull_request_comments USING btree (pull_request_id);


--
-- TOC entry 3367 (class 1259 OID 16584)
-- Name: idx_16471_user_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16471_user_id ON ghtorrent_restore_2015.pull_request_comments USING btree (user_id);


--
-- TOC entry 3368 (class 1259 OID 16543)
-- Name: idx_16478_commit_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16478_commit_id ON ghtorrent_restore_2015.pull_request_commits USING btree (commit_id);


--
-- TOC entry 3371 (class 1259 OID 16547)
-- Name: idx_16482_actor_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16482_actor_id ON ghtorrent_restore_2015.pull_request_history USING btree (actor_id);


--
-- TOC entry 3374 (class 1259 OID 16549)
-- Name: idx_16482_pull_request_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16482_pull_request_id ON ghtorrent_restore_2015.pull_request_history USING btree (pull_request_id);


--
-- TOC entry 3375 (class 1259 OID 16558)
-- Name: idx_16489_base_commit_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16489_base_commit_id ON ghtorrent_restore_2015.pull_requests USING btree (base_commit_id);


--
-- TOC entry 3376 (class 1259 OID 16563)
-- Name: idx_16489_base_repo_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16489_base_repo_id ON ghtorrent_restore_2015.pull_requests USING btree (base_repo_id);


--
-- TOC entry 3377 (class 1259 OID 16560)
-- Name: idx_16489_head_commit_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16489_head_commit_id ON ghtorrent_restore_2015.pull_requests USING btree (head_commit_id);


--
-- TOC entry 3378 (class 1259 OID 16559)
-- Name: idx_16489_head_repo_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16489_head_repo_id ON ghtorrent_restore_2015.pull_requests USING btree (head_repo_id);


--
-- TOC entry 3381 (class 1259 OID 16557)
-- Name: idx_16489_pullreq_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE UNIQUE INDEX idx_16489_pullreq_id ON ghtorrent_restore_2015.pull_requests USING btree (pullreq_id, base_repo_id);


--
-- TOC entry 3382 (class 1259 OID 16561)
-- Name: idx_16489_user_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16489_user_id ON ghtorrent_restore_2015.pull_requests USING btree (user_id);


--
-- TOC entry 3385 (class 1259 OID 16567)
-- Name: idx_16495_repo_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16495_repo_id ON ghtorrent_restore_2015.repo_labels USING btree (repo_id);


--
-- TOC entry 3388 (class 1259 OID 16578)
-- Name: idx_16501_repo_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16501_repo_id ON ghtorrent_restore_2015.repo_milestones USING btree (repo_id);


--
-- TOC entry 3389 (class 1259 OID 16542)
-- Name: idx_16511_login; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE UNIQUE INDEX idx_16511_login ON ghtorrent_restore_2015.users USING btree (login);


--
-- TOC entry 3394 (class 1259 OID 16546)
-- Name: idx_16520_user_id; Type: INDEX; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE INDEX idx_16520_user_id ON ghtorrent_restore_2015.watchers USING btree (user_id);


--
-- TOC entry 3395 (class 2606 OID 16609)
-- Name: commit_comments commit_comments_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.commit_comments
    ADD CONSTRAINT commit_comments_ibfk_1 FOREIGN KEY (commit_id) REFERENCES ghtorrent_restore_2015.commits(id);


--
-- TOC entry 3396 (class 2606 OID 16614)
-- Name: commit_comments commit_comments_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.commit_comments
    ADD CONSTRAINT commit_comments_ibfk_2 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3397 (class 2606 OID 16619)
-- Name: commit_parents commit_parents_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.commit_parents
    ADD CONSTRAINT commit_parents_ibfk_1 FOREIGN KEY (commit_id) REFERENCES ghtorrent_restore_2015.commits(id);


--
-- TOC entry 3398 (class 2606 OID 16624)
-- Name: commit_parents commit_parents_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.commit_parents
    ADD CONSTRAINT commit_parents_ibfk_2 FOREIGN KEY (parent_id) REFERENCES ghtorrent_restore_2015.commits(id);


--
-- TOC entry 3399 (class 2606 OID 16629)
-- Name: commits commits_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.commits
    ADD CONSTRAINT commits_ibfk_1 FOREIGN KEY (author_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3400 (class 2606 OID 16634)
-- Name: commits commits_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.commits
    ADD CONSTRAINT commits_ibfk_2 FOREIGN KEY (committer_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3401 (class 2606 OID 16639)
-- Name: commits commits_ibfk_3; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.commits
    ADD CONSTRAINT commits_ibfk_3 FOREIGN KEY (project_id) REFERENCES ghtorrent_restore_2015.projects(id);


--
-- TOC entry 3402 (class 2606 OID 16644)
-- Name: followers followers_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.followers
    ADD CONSTRAINT followers_ibfk_1 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3403 (class 2606 OID 16649)
-- Name: followers followers_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.followers
    ADD CONSTRAINT followers_ibfk_2 FOREIGN KEY (follower_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3404 (class 2606 OID 16654)
-- Name: forks forks_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.forks
    ADD CONSTRAINT forks_ibfk_1 FOREIGN KEY (forked_project_id) REFERENCES ghtorrent_restore_2015.projects(id);


--
-- TOC entry 3405 (class 2606 OID 16659)
-- Name: forks forks_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.forks
    ADD CONSTRAINT forks_ibfk_2 FOREIGN KEY (forked_from_id) REFERENCES ghtorrent_restore_2015.projects(id);


--
-- TOC entry 3406 (class 2606 OID 16669)
-- Name: issue_comments issue_comments_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.issue_comments
    ADD CONSTRAINT issue_comments_ibfk_2 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3407 (class 2606 OID 16679)
-- Name: issue_events issue_events_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.issue_events
    ADD CONSTRAINT issue_events_ibfk_2 FOREIGN KEY (actor_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3408 (class 2606 OID 16684)
-- Name: issue_labels issue_labels_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.issue_labels
    ADD CONSTRAINT issue_labels_ibfk_1 FOREIGN KEY (label_id) REFERENCES ghtorrent_restore_2015.repo_labels(id);


--
-- TOC entry 3409 (class 2606 OID 16694)
-- Name: issues issues_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.issues
    ADD CONSTRAINT issues_ibfk_1 FOREIGN KEY (repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


--
-- TOC entry 3410 (class 2606 OID 16699)
-- Name: issues issues_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.issues
    ADD CONSTRAINT issues_ibfk_2 FOREIGN KEY (reporter_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3411 (class 2606 OID 16704)
-- Name: issues issues_ibfk_3; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.issues
    ADD CONSTRAINT issues_ibfk_3 FOREIGN KEY (assignee_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3412 (class 2606 OID 16709)
-- Name: issues issues_ibfk_4; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.issues
    ADD CONSTRAINT issues_ibfk_4 FOREIGN KEY (pull_request_id) REFERENCES ghtorrent_restore_2015.pull_requests(id);


--
-- TOC entry 3413 (class 2606 OID 16714)
-- Name: organization_members organization_members_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.organization_members
    ADD CONSTRAINT organization_members_ibfk_1 FOREIGN KEY (org_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3414 (class 2606 OID 16719)
-- Name: organization_members organization_members_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.organization_members
    ADD CONSTRAINT organization_members_ibfk_2 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3415 (class 2606 OID 16724)
-- Name: project_commits project_commits_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.project_commits
    ADD CONSTRAINT project_commits_ibfk_1 FOREIGN KEY (project_id) REFERENCES ghtorrent_restore_2015.projects(id);


--
-- TOC entry 3416 (class 2606 OID 16729)
-- Name: project_commits project_commits_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.project_commits
    ADD CONSTRAINT project_commits_ibfk_2 FOREIGN KEY (commit_id) REFERENCES ghtorrent_restore_2015.commits(id);


--
-- TOC entry 3417 (class 2606 OID 16734)
-- Name: project_members project_members_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.project_members
    ADD CONSTRAINT project_members_ibfk_1 FOREIGN KEY (repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


--
-- TOC entry 3418 (class 2606 OID 16739)
-- Name: project_members project_members_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.project_members
    ADD CONSTRAINT project_members_ibfk_2 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3419 (class 2606 OID 16744)
-- Name: projects projects_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.projects
    ADD CONSTRAINT projects_ibfk_1 FOREIGN KEY (owner_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3420 (class 2606 OID 16749)
-- Name: projects projects_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.projects
    ADD CONSTRAINT projects_ibfk_2 FOREIGN KEY (forked_from) REFERENCES ghtorrent_restore_2015.projects(id);


--
-- TOC entry 3421 (class 2606 OID 16754)
-- Name: pull_request_comments pull_request_comments_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_comments
    ADD CONSTRAINT pull_request_comments_ibfk_1 FOREIGN KEY (pull_request_id) REFERENCES ghtorrent_restore_2015.pull_requests(id);


--
-- TOC entry 3422 (class 2606 OID 16759)
-- Name: pull_request_comments pull_request_comments_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_comments
    ADD CONSTRAINT pull_request_comments_ibfk_2 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3423 (class 2606 OID 16764)
-- Name: pull_request_comments pull_request_comments_ibfk_3; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_comments
    ADD CONSTRAINT pull_request_comments_ibfk_3 FOREIGN KEY (commit_id) REFERENCES ghtorrent_restore_2015.commits(id);

-- CUSTOM
ALTER TABLE ONLY ghtorrent_restore_2015.extractions
    ADD CONSTRAINT extraction_metadata_ibfk_1 FOREIGN KEY (project_id) REFERENCES ghtorrent_restore_2015.projects(id);


--
-- TOC entry 3424 (class 2606 OID 16769)
-- Name: pull_request_commits pull_request_commits_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_commits
    ADD CONSTRAINT pull_request_commits_ibfk_1 FOREIGN KEY (pull_request_id) REFERENCES ghtorrent_restore_2015.pull_requests(id);


--
-- TOC entry 3425 (class 2606 OID 16774)
-- Name: pull_request_commits pull_request_commits_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_commits
    ADD CONSTRAINT pull_request_commits_ibfk_2 FOREIGN KEY (commit_id) REFERENCES ghtorrent_restore_2015.commits(id);


--
-- TOC entry 3426 (class 2606 OID 16779)
-- Name: pull_request_history pull_request_history_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_history
    ADD CONSTRAINT pull_request_history_ibfk_1 FOREIGN KEY (pull_request_id) REFERENCES ghtorrent_restore_2015.pull_requests(id);


--
-- TOC entry 3427 (class 2606 OID 16784)
-- Name: pull_request_history pull_request_history_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_history
    ADD CONSTRAINT pull_request_history_ibfk_2 FOREIGN KEY (actor_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3428 (class 2606 OID 16789)
-- Name: pull_requests pull_requests_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests
    ADD CONSTRAINT pull_requests_ibfk_1 FOREIGN KEY (head_repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


--
-- TOC entry 3429 (class 2606 OID 16794)
-- Name: pull_requests pull_requests_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests
    ADD CONSTRAINT pull_requests_ibfk_2 FOREIGN KEY (base_repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


--
-- TOC entry 3430 (class 2606 OID 16799)
-- Name: pull_requests pull_requests_ibfk_3; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests
    ADD CONSTRAINT pull_requests_ibfk_3 FOREIGN KEY (head_commit_id) REFERENCES ghtorrent_restore_2015.commits(id);


--
-- TOC entry 3431 (class 2606 OID 16804)
-- Name: pull_requests pull_requests_ibfk_4; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests
    ADD CONSTRAINT pull_requests_ibfk_4 FOREIGN KEY (base_commit_id) REFERENCES ghtorrent_restore_2015.commits(id);


--
-- TOC entry 3432 (class 2606 OID 16809)
-- Name: pull_requests pull_requests_ibfk_5; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.pull_requests
    ADD CONSTRAINT pull_requests_ibfk_5 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


--
-- TOC entry 3433 (class 2606 OID 16814)
-- Name: repo_labels repo_labels_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.repo_labels
    ADD CONSTRAINT repo_labels_ibfk_1 FOREIGN KEY (repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


--
-- TOC entry 3434 (class 2606 OID 16819)
-- Name: repo_milestones repo_milestones_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.repo_milestones
    ADD CONSTRAINT repo_milestones_ibfk_1 FOREIGN KEY (repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


--
-- TOC entry 3435 (class 2606 OID 16824)
-- Name: watchers watchers_ibfk_1; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.watchers
    ADD CONSTRAINT watchers_ibfk_1 FOREIGN KEY (repo_id) REFERENCES ghtorrent_restore_2015.projects(id);


--
-- TOC entry 3436 (class 2606 OID 16829)
-- Name: watchers watchers_ibfk_2; Type: FK CONSTRAINT; Schema: ghtorrent_restore_2015; Owner: -
--

ALTER TABLE ONLY ghtorrent_restore_2015.watchers
    ADD CONSTRAINT watchers_ibfk_2 FOREIGN KEY (user_id) REFERENCES ghtorrent_restore_2015.users(id);


-- CUSTOM

ALTER TABLE ONLY ghtorrent_restore_2015.metrics_log
    ADD CONSTRAINT metrics_log_ibfk_1 FOREIGN KEY (repo_id) REFERENCES ghtorrent_restore_2015.projects(id);

ALTER TABLE ONLY ghtorrent_restore_2015.metrics_log
    ADD CONSTRAINT metrics_log_ibfk_2 FOREIGN KEY (metric_id) REFERENCES ghtorrent_restore_2015.metrics(id);


-- Completed on 2023-04-12 17:21:00

--
-- PostgreSQL database dump complete
--

