"""
Source's Template

should be used to as a template to implement the needed functionality to add MetaItem and OSSoftware from the external source (github,{source}, gitlab, custom...etc). 
"""

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

API_BASE_URL = "https://example.org/api/v1"

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
    """Get the Individual's data from {source} API and return it as an Owner Model"""

    res_dict: dict[str, Any] = {}
    match meta_item.owner_type:
        case OwnerType.Organization:
            res = get(url=f"{API_BASE_URL}/orgs/{meta_item.owner_username}")    
            if res.status_code != 200:
                return None
            res_dict = res.json()

        # As I can access Organizations' data only, so I use the default case: _, to handle any case in the future when edit the OwnerType
        case OwnerType.Individual:
            pass
        # case _:
        #     logger.error(f"Unknown Owner type: {meta_item.owner_type}")
        #     return None

    new_meta_item = get_new_meta_item(meta_list_key, meta_item, res_dict)
    return new_meta_item

def get_new_meta_item(meta_list_key: str, meta_item: MetaItemSchemas.JSONSchema, api_response: dict[str, Any]) -> MetaItemModel | None: # pyright:ignore[reportExplicitAny]
    """Get the needed data from {source} API into the MetaItem Model"""
    try:
        new_meta_item = MetaItemModel()
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
        logger.error(f"Error Inserting OSS for Unique key Violation OSS from {meta_item.owner_type} meta item", meta_item_owner_username=meta_item.owner_username, repo=repo_dict, error=e)
        return None
    except errors.CheckViolation as e:
        db.rollback()
        logger.error(f"Error Inserting OSS for check Violation OSS from {meta_item.owner_type} meta item", meta_item_owner_username=meta_item.owner_username, repo=repo_dict, error=e)
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"Unknown Error when Inserting OSS from {meta_item.owner_type} meta item", meta_item_owner_username=meta_item.owner_username, repo=repo_dict, error=e)
        return None

def get_repos_from_source(meta_item: MetaItemModel):
    res_arr: list[dict[str, Any]] = []
    ### Get all repos
    match meta_item.owner_type:
        case OwnerType.Organization:
            res = get(url=f"{API_BASE_URL}/orgs/{meta_item.owner_username}/repos")    
            if res.status_code != 200:
                return None
            res_arr = res.json()
        # As I can access Organizations' data only, so I use the default case: _, to handle any case in the future when edit the OwnerType
        # case OwnerType.Individual:
            # logger.error("Can't get Individual data without authentication token")
            # return None
        case _:
            logger.error("Can't get Individual's data without authentication token")
            return None

    return res_arr


def get_new_oss(meta_item: MetaItemModel, repo_dict: dict[str, Any]) -> OSSoftwareModel | None: # pyright:ignore[reportExplicitAny]
    """Get the needed data from {source} API response - an item from repos array - to create a OSS model."""
    try:
        oss = OSSoftwareModel()
        ####
        return oss

    except KeyError as e:
        logger.error("owner's repo data keys have changed, so there was an error converting it to an OSS model", error=e)
        return None

    except Exception as e:
        logger.error("Unknown error parsing github API for owners' details", error=e)
        return None
