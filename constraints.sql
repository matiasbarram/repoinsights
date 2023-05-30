\connect ghtorrent_restore_2015


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


-- Completed on 2023-04-12 17:21:00

--
-- PostgreSQL database dump complete
--

-- CUSTOM METRICS TABLES


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



-- Creación del usuario de solo lectura
CREATE ROLE readonly_user WITH LOGIN PASSWORD 'readonly_user_password';

-- Otorgar permisos en el esquema ghtorrent_restore_2015
GRANT USAGE ON SCHEMA ghtorrent_restore_2015 TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA ghtorrent_restore_2015 TO readonly_user;

-- Otorgar permisos en el esquema public
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
