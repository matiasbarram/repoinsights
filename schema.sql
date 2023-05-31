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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL,
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
);


--
-- TOC entry 226 (class 1259 OID 16433)
-- Name: issue_labels; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.issue_labels (
    label_id integer DEFAULT 0 NOT NULL,
    issue_id integer DEFAULT 0 NOT NULL,
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
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
    issue_id integer NOT NULL,
    pull_request boolean NOT NULL,
    pull_request_id integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
);


--
-- TOC entry 230 (class 1259 OID 16451)
-- Name: project_commits; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.project_commits (
    project_id integer DEFAULT 0 NOT NULL,
    commit_id integer DEFAULT 0 NOT NULL,
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
);


--
-- TOC entry 231 (class 1259 OID 16456)
-- Name: project_members; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.project_members (
    repo_id integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL,
    forked_from integer,
    deleted boolean DEFAULT false NOT NULL,
    private boolean DEFAULT false NOT NULL
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
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
    comment_id integer NOT NULL,
    "position" integer,
    body character varying(256),
    commit_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
);


--
-- TOC entry 237 (class 1259 OID 16482)
-- Name: pull_request_history; Type: TABLE; Schema: ghtorrent_restore_2015; Owner: -
--

CREATE TABLE ghtorrent_restore_2015.pull_request_history (
    id integer NOT NULL,
    pull_request_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL,
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL,
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
    ext_ref_id character varying(32) DEFAULT '0' NOT NULL
);


-- CUSTOM

CREATE TABLE ghtorrent_restore_2015.metrics (
    id integer NOT NULL,
    name character varying(255) NOT NULL UNIQUE,
    description character varying(255),
    measurement_type character varying(255) NOT NULL,
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



CREATE TABLE ghtorrent_restore_2015.project_metrics (
    id INTEGER NOT NULL,
    extraction_id INTEGER NOT NULL DEFAULT 0,
    metric_id INTEGER NOT NULL,
    value VARCHAR(255), -- Store all values as strings, convert as needed
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE SEQUENCE ghtorrent_restore_2015.project_metrics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE ghtorrent_restore_2015.project_metrics_id_seq OWNED BY ghtorrent_restore_2015.project_metrics.id;

CREATE TABLE ghtorrent_restore_2015.pull_request_metrics (
    id INTEGER NOT NULL,
    extraction_id INTEGER NOT NULL,
    pull_request_id INTEGER NOT NULL,
    metric_id INTEGER NOT NULL,
    value VARCHAR(255), -- Store all values as strings, convert as needed
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


CREATE SEQUENCE ghtorrent_restore_2015.pull_request_metrics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE ghtorrent_restore_2015.pull_request_metrics_id_seq OWNED BY ghtorrent_restore_2015.pull_request_metrics.id;


CREATE TABLE ghtorrent_restore_2015.issue_metrics (
    id INTEGER NOT NULL,
    extraction_id INTEGER NOT NULL,
    issue_id INTEGER NOT NULL,
    metric_id INTEGER NOT NULL,
    value VARCHAR(255), -- Store all values as strings, convert as needed
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE SEQUENCE ghtorrent_restore_2015.issue_metrics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE ghtorrent_restore_2015.issue_metrics_id_seq OWNED BY ghtorrent_restore_2015.issue_metrics.id;

CREATE TABLE ghtorrent_restore_2015.user_metrics (
    id INTEGER NOT NULL,
    extraction_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    metric_id INTEGER NOT NULL,
    value VARCHAR(255), -- Store all values as strings, convert as needed
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE SEQUENCE ghtorrent_restore_2015.user_metrics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE ghtorrent_restore_2015.user_metrics_id_seq OWNED BY ghtorrent_restore_2015.user_metrics.id;


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

-- pull_request_comments_id_seq
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_comments ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.pull_request_comments_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_comments
    ADD CONSTRAINT idx_12396_primary PRIMARY KEY (id);


ALTER TABLE ONLY ghtorrent_restore_2015.issue_comments ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.issue_comments_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.issue_comments
    ADD CONSTRAINT idx_12397_primary PRIMARY KEY (id);


ALTER TABLE ONLY ghtorrent_restore_2015.project_metrics ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.project_metrics_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.project_metrics
    ADD CONSTRAINT idx_12398_primary PRIMARY KEY (id);

ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_metrics ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.pull_request_metrics_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.pull_request_metrics
    ADD CONSTRAINT idx_12399_primary PRIMARY KEY (id);

ALTER TABLE ONLY ghtorrent_restore_2015.issue_metrics ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.issue_metrics_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.issue_metrics
    ADD CONSTRAINT idx_12400_primary PRIMARY KEY (id);

ALTER TABLE ONLY ghtorrent_restore_2015.user_metrics ALTER COLUMN id SET DEFAULT nextval('ghtorrent_restore_2015.user_metrics_id_seq'::regclass);
ALTER TABLE ONLY ghtorrent_restore_2015.user_metrics
    ADD CONSTRAINT idx_12401_primary PRIMARY KEY (id);

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

