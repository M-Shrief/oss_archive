from httpx import get
from typing import Any
from sqlalchemy.orm import Session
# from sqlalchemy import select, delete, update
# from sqlalchemy import exc 
from psycopg import errors
###
from oss_archive.utils.logger import logger
from oss_archive.utils.formatter import format_repo_fullname
from oss_archive.database.models import MetaItem as MetaItemModel, OSSoftware as OSSoftwareModel
from oss_archive.schemas import meta_item as MetaItemSchemas
from oss_archive.schemas.general import OwnerType
from oss_archive.seeders.helpers import does_meta_item_exists, does_oss_exists, should_apply_action_on_oss

API_BASE_URL = "https://api.github.com"


def seed_meta_item(meta_list_key: str, meta_item: MetaItemSchemas.JSONSchema, db: Session) -> MetaItemModel | None:     # This is a protocol member
    """Seed a single MetaItem from the meta list's items in its JSON file"""
    try:
        ### Used 2 different conditions block to differntiate the logs.
        if not meta_item.reviewed:
            logger.info(f"Skipped {meta_item.owner_username}'s meta item, because it's not reviewed")
            return None

        meta_item_does_exists = does_meta_item_exists(meta_item.owner_username, db)
        if meta_item_does_exists:
            logger.info(f"Skipped {meta_item.owner_username}'s meta item, because it's already seeded")
            return None

        
        new_meta_item = get_meta_item_from_source(meta_list_key, meta_item)

        db.add(new_meta_item)
        db.commit()
        # db.refresh()
        return new_meta_item        

    except errors.UniqueViolation as e:
        db.rollback()
        logger.error(f"Error Inserting meta_item for Unique key Violation, using {meta_item.owner_type} meta item", meta_list_key=meta_list_key, meta_item=meta_item, error=e)
        return None
    except errors.CheckViolation as e:
        db.rollback()
        logger.error(f"Error Inserting meta_item for check Violation, using {meta_item.owner_type} meta item", meta_list_key=meta_list_key, meta_item=meta_item, error=e)
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"Unknown Error when Inserting meta_item, using {meta_item.owner_type} meta item", meta_list_key=meta_list_key, meta_item=meta_item, error=e)
        return None

def get_meta_item_from_source(meta_list_key: str, meta_item: MetaItemSchemas.JSONSchema)-> MetaItemModel | None:
    """Get the Organization/Individual's data from Github API and return it as an Owner Model"""
    match meta_item.owner_type:
        case OwnerType.Organization:
            res = get(url=f"{API_BASE_URL}/orgs/{meta_item.owner_username}")
        case OwnerType.Individual:
            res = get(url=F"{API_BASE_URL}/users/{meta_item.owner_username}")
        case _:
            logger.error(f"Unknown Owner type: {meta_item.owner_type}")
            return None
            
    if res.status_code != 200:
        return None
    res_dict: dict[str, Any] = res.json()

    new_meta_item = get_new_meta_item(meta_list_key, meta_item, res_dict)
    return new_meta_item

def get_new_meta_item(meta_list_key: str, meta_item: MetaItemSchemas.JSONSchema, api_response: dict[str, Any]) -> MetaItemModel | None: # pyright:ignore[reportExplicitAny]
    """Get the needed data from Github API into the MetaItem Model"""
    try:
        new_meta_item = MetaItemModel()
        new_meta_item.priority = meta_item.priority
        new_meta_item.reviewed = meta_item.reviewed
        ### URLs
        new_meta_item.html_url = api_response.get("html_url")
        ### Sources
        new_meta_item.source = meta_item.source
        new_meta_item.other_sources = meta_item.other_sources
        ### Actions
        new_meta_item.actions = meta_item.actions
        new_meta_item.actions_on = meta_item.actions_on
        ### MetaItemModel's Data        
        new_meta_item.owner_username = meta_item.owner_username
        new_meta_item.owner_name = api_response.get("name")
        new_meta_item.owner_type = meta_item.owner_type # pyright: ignore[reportAttributeAccessIssue]
        new_meta_item.owner_created_at = api_response.get("created_at")
        new_meta_item.owner_updated_at = api_response.get("updated_at")

        ### Relations
        new_meta_item.meta_list_key = meta_list_key

        return new_meta_item

    except KeyError as e:
        logger.error("owner's data keys have changed, so there was an error converting it to an Owner model", error=e)
        return None

    except Exception as e:
        logger.error("Unknown error parsing github API for owners' details", error=e)
        return None


def seed_os_softwares(meta_item: MetaItemModel, db: Session) -> list[OSSoftwareModel] | None:
    repos_arr = get_repos_from_source(meta_item)
    if repos_arr is None:
        return None

    new_os_softwares: list[OSSoftwareModel] = []
    for repo in repos_arr:
        should_apply_on = should_apply_action_on_oss(meta_item, repo)
        if not should_apply_on:
            continue

        seeded_oss = seed_oss(meta_item, repo, db)
        if seeded_oss is None:
            continue

        new_os_softwares.append(seeded_oss)

    return new_os_softwares

def seed_oss(meta_item: MetaItemModel, repo_dict: dict[str, Any], db: Session):
    try:
        repo_name = repo_dict.get("name")
        if repo_name is None:
            return None
        oss_fullname = format_repo_fullname(meta_item.owner_username, repo_name)

        oss_does_exists = does_oss_exists(oss_fullname, db)
        if oss_does_exists:
            return None

        new_oss = get_new_oss(meta_item, repo_dict)
        if new_oss is None:
            return None
        
        db.add(new_oss)
        db.commit()
        
        return new_oss
    except errors.UniqueViolation as e:
        db.rollback()
        logger.error(f"Error Inserting OSS for Unique key Violation OSS from {meta_item.owner_type} meta item", meta_item_owner_username=meta_item.owner_username, error=e)
        return None
    except errors.CheckViolation as e:
        db.rollback()
        logger.error(f"Error Inserting OSS for check Violation OSS from {meta_item.owner_type} meta item", meta_item_owner_username=meta_item.owner_username, error=e)
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"Unknown Error when Inserting OSS from {meta_item.owner_type} meta item", meta_item_owner_username=meta_item.owner_username, error=e)
        return None

def get_repos_from_source(meta_item: MetaItemModel):
    match meta_item.owner_type:
        case OwnerType.Organization:
            res = get(url=f"{API_BASE_URL}/orgs/{meta_item.owner_username}/repos")    
        case OwnerType.Individual:
            res = get(url=f"{API_BASE_URL}/users/{meta_item.owner_username}/repos")    
        case _:
            logger.error(f"Uknown OwnerType: {meta_item.owner_type}")
            return None

    if res.status_code != 200:
        return None
    res_arr: list[dict[str, Any]] = res.json()
    return res_arr


def get_new_oss(meta_item: MetaItemModel, repo_dict: dict[str, Any]) -> OSSoftwareModel | None: # pyright:ignore[reportExplicitAny]
    """Get the needed data from Github API response - an item from repos array - to create a OSS model."""
    try:
        oss = OSSoftwareModel()
        oss.name = repo_dict.get("name") # pyright:ignore[reportAttributeAccessIssue]
        oss.fullname = format_repo_fullname(meta_item.owner_username, oss.name)
        oss.description = repo_dict.get("description")
        oss.topics = repo_dict.get("topics") # pyright:ignore[reportAttributeAccessIssue]
        oss.html_url = repo_dict.get("html_url")
        oss.clone_url = repo_dict.get("clone_url")
        oss.created_at_source = repo_dict.get("created_at") 
        oss.updated_at_source = repo_dict.get("updated_at")

        # Relations
        oss.meta_list_key = meta_item.meta_list_key
        oss.meta_item_id = meta_item.id
        repo_license = repo_dict.get("license")
        if repo_license is not None and repo_license["key"] != "other":
            oss.license_key = repo_license["key"]

        return oss

    except KeyError as e:
        logger.error("owner's repo data keys have changed, so there was an error converting it to an OSS model", error=e)
        return None

    except Exception as e:
        logger.error("Unknown error parsing github API for owners' details", error=e)
        return None

