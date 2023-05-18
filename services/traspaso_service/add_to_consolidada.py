from typing import List, Dict, Any, Tuple, Union
from services.traspaso_service.traspaso.common_clases import Cache, DatabaseHandler
from services.traspaso_service.db_connector.models import (
    User,
    Project,
    Commit,
    CommitComment,
    CommitParent,
    Follower,
    Fork,
    Issue,
    IssueComment,
    IssueEvent,
    IssueLabel,
    OrganizationMember,
    ProjectCommit,
    ProjectMember,
    PullRequest,
    PullRequestComment,
    PullRequestCommit,
    PullRequestHistory,
    RepoLabel,
    RepoMilestone,
    Watcher,
    Extraction,
)

from services.traspaso_service.traspaso.entity_data import EntityData
from pprint import pprint
from loguru import logger


class DataHandler:
    def __init__(self, db: DatabaseHandler) -> None:
        pass

    def find_by_attributes(self, session, entity_class, **kwargs):
        return session.query(entity_class).filter_by(**kwargs).first()


class EntityHandler:
    def __init__(self, db: DatabaseHandler, cache: Cache, entity_data: Dict) -> None:
        self.db = db
        self.cache = cache
        self.data_handler = DataHandler(db)
        self.entity_data = entity_data

    def get_value_from_consolidada(self, entity_class, entity, attr_name, attr_value):
        # get consolidada id
        sks = self.entity_data[entity_class]["search_keys"]
        filters = self.create_filters(entity, sks)
        exist_entity = self.search_entity(entity_class, entity, filters)
        if exist_entity is None:
            logger.error(
                "No se encontro el {attr_name}/{attr_value} en la base de datos consolidada",
                attr_value=attr_value,
                attr_name=attr_name,
            )
            return None
        logger.debug("FOUND in consolidada! \t {value}", value=exist_entity.__dict__)
        cache_map = self.entity_data[entity_class]["cache_map"]
        cache_map[entity.id] = exist_entity.id
        return exist_entity

    def get_value_from_temp(self, entity_class, attr_name, attr_value):
        temp_entity = self.data_handler.find_by_attributes(
            session=self.db.session_temp,
            entity_class=entity_class,
            **{attr_name: attr_value},
        )
        if temp_entity is None:
            logger.error(
                "No se encontro el {attr_name}/{attr_value} en la base de datos",
                attr_value=attr_value,
                attr_name=attr_name,
            )
            return None
        logger.debug("FOUND in temp! \t {value}", value=temp_entity.__dict__)
        consolidada_entity = self.get_value_from_consolidada(
            entity_class, temp_entity, attr_name, attr_value
        )
        if consolidada_entity is None:
            return None
        return consolidada_entity.id

    def handle_not_found_in_map(self, entity_class, attr_name, attr_value):
        if attr_value is None:
            return None
        temp_entity = self.get_value_from_temp(entity_class, attr_name, attr_value)
        if temp_entity is None:
            return None
        consolidada_entity = self.get_value_from_consolidada(
            entity_class, temp_entity, attr_name, attr_value
        )
        if consolidada_entity is None:
            return None
        return consolidada_entity.id

    def create_filters(self, entity, sk):
        search_filters = {}
        for key in sk:
            if isinstance(key, tuple):
                attr_name, cache_map_lookup, entity_class = key
                attr_value = getattr(entity, attr_name)
                if attr_value is not None:
                    if attr_value in cache_map_lookup:
                        search_filters[attr_name] = cache_map_lookup[attr_value]
                    # si el attr_value no está en su caché
                    # head_repo_id 7 en la cache self.cache.project
                    else:
                        logger.warning(
                            "{entity} \t No se encontro el {attr_name}/{attr_value} en el cache",
                            entity=entity.__dict__,
                            attr_value=attr_value,
                            attr_name=attr_name,
                        )
                        entity_id = self.entity_data[entity_class].get("id") or "id"
                        value_id = self.get_value_from_temp(
                            entity_class, entity_id, attr_value
                        )
                        if value_id is not None:
                            search_filters[attr_name] = value_id
            else:
                search_filters[key] = getattr(entity, key)
        return search_filters

    def search_entity(self, entity_class, entity, filters):
        # Verificar si la entidad ya existe en la base de datos consolidada
        exist_entity = self.data_handler.find_by_attributes(
            session=self.db.session_consolidada, entity_class=entity_class, **filters
        )
        return exist_entity

    def create_entity(self, entity_class, entity, filters, cache_map=None):
        # Crear la entidad en la base de datos consolidada
        logger.debug("CREATING! \t {entity}", entity=entity.__dict__)
        entity_id = self.entity_data[entity_class].get("id") or "id"
        old_id = getattr(entity, entity_id)
        new_entity = entity_class(**filters)
        self.db.session_consolidada.add(new_entity)
        self.db.session_consolidada.commit()

        if cache_map is not None:
            cache_map[old_id] = new_entity.id
        return new_entity

    def add_entities(
        self, entity_class, entities, search_keys, add_keys, cache_map=None
    ):
        for entity in entities:
            # TODO Obtener desde la base de datos el valor de los
            # atributos que son llaves foraneas si es que no estan en el cache
            filters = self.create_filters(entity, search_keys)
            exist = self.search_entity(entity_class, entity, filters)
            if exist is None:
                filters = self.create_filters(entity, add_keys)
                if filters is not None:
                    self.create_entity(entity_class, entity, filters, cache_map)
            else:
                if cache_map is not None:
                    cache_map[entity.id] = exist.id


class ConsolidatedClient:
    def __init__(self, uuid: str, db: DatabaseHandler) -> None:
        self.uuid = uuid
        self.db = db

        self.cache = Cache()
        self.entity_data_handler = EntityData(cache=self.cache)
        self.entity_data = self.entity_data_handler.get_entity_data()
        self.entity_handler = EntityHandler(self.db, self.cache, self.entity_data)

    def add_users(self, users: List[User]):
        self.entity_handler.add_entities(
            entity_class=User,
            entities=users,
            search_keys=self.entity_data[User]["search_keys"],
            add_keys=self.entity_data[User]["add_keys"],
            cache_map=self.entity_data[User]["cache_map"],
        )
        pprint(self.cache.user_id_map)

    def add_projects(self, projects: List[Project]):
        def add_project(projects, lambda_function):
            filtered_projects = list(filter(lambda_function, projects))
            self.entity_handler.add_entities(
                entity_class=Project,
                entities=filtered_projects,
                search_keys=self.entity_data[Project]["search_keys"],
                add_keys=self.entity_data[Project]["add_keys"],
                cache_map=self.entity_data[Project]["cache_map"],
            )

        add_project(
            projects, lambda x: x.forked_from is None
        )  # Agregar proyectos principales
        add_project(
            projects, lambda x: x.forked_from is not None
        )  # Agregar proyectos bifurcados

        pprint(self.cache.project_id_map)

    def add_extractions(self, extractions: List[Extraction]):
        self.entity_handler.add_entities(
            entity_class=Extraction,
            entities=extractions,
            search_keys=self.entity_data[Extraction]["search_keys"],
            add_keys=self.entity_data[Extraction]["add_keys"],
        )

    def add_project_members(self, project_members: List[ProjectMember]):
        self.entity_handler.add_entities(
            entity_class=ProjectMember,
            entities=project_members,
            search_keys=self.entity_data[ProjectMember]["search_keys"],
            add_keys=self.entity_data[ProjectMember]["add_keys"],
        )

    def add_labels(self, labels: List[RepoLabel]):
        self.entity_handler.add_entities(
            entity_class=RepoLabel,
            entities=labels,
            search_keys=self.entity_data[RepoLabel]["search_keys"],
            add_keys=self.entity_data[RepoLabel]["add_keys"],
            cache_map=self.entity_data[RepoLabel]["cache_map"],
        )
        pprint(self.cache.label_id_map)

    def add_milestones(self, milestones: List[RepoMilestone]):
        self.entity_handler.add_entities(
            entity_class=RepoMilestone,
            entities=milestones,
            search_keys=self.entity_data[RepoMilestone]["search_keys"],
            add_keys=self.entity_data[RepoMilestone]["add_keys"],
        )

    def add_watchers(self, watchers: List[Watcher]):
        self.entity_handler.add_entities(
            entity_class=Watcher,
            entities=watchers,
            search_keys=self.entity_data[Watcher]["search_keys"],
            add_keys=self.entity_data[Watcher]["add_keys"],
        )

    def add_followers(self, followers: List[Follower]):
        self.entity_handler.add_entities(
            entity_class=Follower,
            entities=followers,
            search_keys=self.entity_data[Follower]["search_keys"],
            add_keys=self.entity_data[Follower]["add_keys"],
        )

    def add_commits(self, commits: List[Commit]):
        self.entity_handler.add_entities(
            entity_class=Commit,
            entities=commits,
            search_keys=self.entity_data[Commit]["search_keys"],
            add_keys=self.entity_data[Commit]["add_keys"],
            cache_map=self.entity_data[Commit]["cache_map"],
        )

    def add_commit_comments(self, commit_comments: List[CommitComment]):
        self.entity_handler.add_entities(
            entity_class=CommitComment,
            entities=commit_comments,
            search_keys=self.entity_data[CommitComment]["search_keys"],
            add_keys=self.entity_data[CommitComment]["add_keys"],
        )

    def add_commit_parents(self, commit_parents: List[CommitParent]):
        self.entity_handler.add_entities(
            entity_class=CommitParent,
            entities=commit_parents,
            search_keys=self.entity_data[CommitParent]["search_keys"],
            add_keys=self.entity_data[CommitParent]["add_keys"],
        )

    def add_pull_requests(self, pull_requests: List[PullRequest]):
        self.entity_handler.add_entities(
            entity_class=PullRequest,
            entities=pull_requests,
            search_keys=self.entity_data[PullRequest]["search_keys"],
            add_keys=self.entity_data[PullRequest]["add_keys"],
            cache_map=self.cache.pull_request_id_map,
        )

    def add_pull_request_comments(
        self, pull_request_comments: List[PullRequestComment]
    ):
        self.entity_handler.add_entities(
            entity_class=PullRequestComment,
            entities=pull_request_comments,
            search_keys=self.entity_data[PullRequestComment]["search_keys"],
            add_keys=self.entity_data[PullRequestComment]["add_keys"],
        )

    def add_pull_request_history(self, pull_request_history: List[PullRequestHistory]):
        self.entity_handler.add_entities(
            entity_class=PullRequestHistory,
            entities=pull_request_history,
            search_keys=self.entity_data[PullRequestHistory]["search_keys"],
            add_keys=self.entity_data[PullRequestHistory]["add_keys"],
        )

    def add_issues(self, issues: List[Issue]):
        self.entity_handler.add_entities(
            entity_class=Issue,
            entities=issues,
            search_keys=self.entity_data[Issue]["search_keys"],
            add_keys=self.entity_data[Issue]["add_keys"],
            cache_map=self.entity_data[Issue]["cache_map"],
        )

    def add_issue_comments(self, issue_comments: List[IssueComment]):
        self.entity_handler.add_entities(
            entity_class=IssueComment,
            entities=issue_comments,
            search_keys=self.entity_data[IssueComment]["search_keys"],
            add_keys=self.entity_data[IssueComment]["add_keys"],
        )

    def add_issue_events(self, issue_events: List[IssueEvent]):
        self.entity_handler.add_entities(
            entity_class=IssueEvent,
            entities=issue_events,
            search_keys=self.entity_data[IssueEvent]["search_keys"],
            add_keys=self.entity_data[IssueEvent]["add_keys"],
        )

    def add_issue_labels(self, issue_labels: List[IssueLabel]):
        self.entity_handler.add_entities(
            entity_class=IssueLabel,
            entities=issue_labels,
            search_keys=self.entity_data[IssueLabel]["search_keys"],
            add_keys=self.entity_data[IssueLabel]["add_keys"],
        )
