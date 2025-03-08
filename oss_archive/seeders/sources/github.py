from httpx import get
from typing import List, Dict, Any
from sqlalchemy.orm import Session
###
from oss_archive.database.models import Owner, OSSoftware
from oss_archive.components.meta_lists.schema import MetaItem, DownloadActions
from oss_archive.utils.schemas import OwnerType
from oss_archive.utils.logger import logger
from oss_archive.utils.formatter import format_repo_fullname


API_BASE_URL = "https://api.github.com"


def add_meta_item(meta_list_key: str, meta_item: MetaItem, db: Session) -> (Owner | None, List[OSSoftware] | None):
    owner = add_owner_from_meta_item(meta_list_key, meta_item, db)
    if owner is None:
        logger.error("Couldn't add meta item", meta_item=meta_item)
        return None, None
    logger.info("added new owner successfully", owner_id=owner.id)

    os_softwares = add_owner_repos(meta_list_key, meta_item, owner, db)
    if os_softwares is None: 
        logger.error("Couldn't add Owner's repos", owner=owner)
        return owner, None
    logger.info("added new owner's open-source softwares", owner_id=owner.id, os_softwares_count=len(os_softwares))
    return owner, os_softwares

def add_owner_from_meta_item(meta_list_key: str, meta_item: MetaItem, db: Session) -> Owner | None:
    match meta_item.type:
        case OwnerType.Organization:
            owner = get_owner_from_org(meta_list_key, meta_item)
            if owner is None:
                return None
            db.add(owner)
            db.commit()
            db.refresh(owner)
            return owner
        case OwnerType.Individual:
            owner = get_owner_from_user(meta_list_key, meta_item)
            if owner is None:
                return None
            db.add(owner)
            db.commit()
            db.refresh(owner)
            return owner
        case _:
            logger.error("Unknown Owner's type", meta_item= meta_item, unknown_type=meta_item.type)
            return None

def add_owner_repos(meta_list_key: str, meta_item: MetaItem, owner: Owner, db: Session) -> List[OSSoftware] | None:
    os_softwares = get_owner_repos(meta_list_key, meta_item, owner)
    if os_softwares is None:
        return None
    db.add_all(os_softwares)
    db.commit()
    new_os_softwares: List[OSSoftware] = []
    for oss in os_softwares:
        db.refresh(oss)
        new_os_softwares.append(oss)
    return new_os_softwares



def get_owner_from_org(meta_list_key: str, meta_item: MetaItem)->Owner | None:
    """Get the Organization's data from codeberg API and return it as an Owner Model"""
    global API_BASE_URL

    res = get(url=f"{API_BASE_URL}/orgs/{meta_item.owner}")    
    if res.status_code != 200:
        return None
    res_dict = res.json()

    org = __get_new_owner(meta_list_key, meta_item, res_dict)
    return org


def get_owner_from_user(meta_list_key: str, meta_item: MetaItem)-> Owner | None:
    """Get the User's data from github API and return it as an Owner Model"""
    global API_BASE_URL

    res = get(url=F"{API_BASE_URL}/users/{meta_item.owner}")
    if res.status_code != 200:
        return None
    res_dict = res.json()
    
    user = __get_new_owner(meta_list_key, meta_item, res_dict)
    return user

def get_owner_repos(meta_list_key: str, meta_item: MetaItem, owner: Owner) -> List[OSSoftware] | None:
    """Get the Organization's repos from GitHub API and return it as a List of OSSoftware Model"""
    global API_BASE_URL

    res = get(url=F"https://api.github.com/users/{owner.username}/repos")
    if res.status_code != 200:
        return None
    res_arr = res.json()

    os_softwares: List[OSSoftware] = []

    match meta_item.actions.download:
        case DownloadActions.All:
            # Get all repos without filtering
            for repo in res_arr:
                oss = __get_new_oss(meta_list_key, owner, repo)
                if oss is None:
                    logger.error("error adding new oss", oss_repo=repo)
                    continue
                os_softwares.append(oss)
        case DownloadActions.Only:
            # get only the selected repos
            filtered_repos = [item for item in res_arr if item["name"] in meta_item.actions.selected_repos]
            for repo in filtered_repos:
                oss = __get_new_oss(meta_list_key, owner, repo)
                if oss is None:
                    logger.error("error adding new oss", oss_repo=repo)
                    continue
                os_softwares.append(oss)
        case DownloadActions.Except:
            # get all repos except the selected repos
            filtered_repos = [item for item in res_arr if item["name"] not in meta_item.actions.selected_repos]
            for repo in filtered_repos:
                oss = __get_new_oss(meta_list_key, owner, repo)
                if oss is None:
                    logger.error("error adding new oss", oss_repo=repo)
                    continue
                os_softwares.append(oss)
        case _:
            logger.error("Download Actions is not specified in the right way.", meta_item_actions=meta_item.actions)
            return None

    if len(os_softwares) == 0:
        return None
    return os_softwares


def __get_new_owner(meta_list_key: str, meta_item: MetaItem, api_org_res: dict[str, Any]) -> Owner | None:
    """Get the needed data from codeberg API into the Owner Model"""
    try:
        owner = Owner()
        owner.oss_list_key = meta_list_key

        owner.source = meta_item.source
        owner.type = meta_item.type
        owner.priority = meta_item.priority
        owner.reviewed = meta_item.reviewed

        owner.username = api_org_res.get("login")
        owner.name = api_org_res.get("name")
        owner.html_url = api_org_res.get("html_url")
        owner.api_url = api_org_res.get("url")
        owner.created_at = api_org_res.get("created_at")
        owner.updated_at = api_org_res.get("updated_at")

        return owner

    except KeyError as e:
        logger.error("owner's data keys have changed, so there was an error converting it to an Owner model", error=e)
        return None

    except Exception as e:
        logger.error("Unknown error parsing github API for owners' details", error=e)
        return None


def __get_new_oss(meta_list_key: str, owner: Owner, api_repo_res: Dict[str, Any]) -> OSSoftware | None:
    """Get the needed data from codeberg API response - from the owner's repo array - to create a OSS model."""
    try:
        oss = OSSoftware()

        oss.oss_list_key = meta_list_key
        oss.owner_id = owner.id
        if api_repo_res.get("license") is not None and api_repo_res.get("license")["key"] != "other":
            oss.license_key = api_repo_res.get("license")["key"]

        oss.name = api_repo_res.get("name")
        oss.fullname = format_repo_fullname(owner.username, api_repo_res.get("name"))
        oss.description = api_repo_res.get("description")
        oss.topics = api_repo_res.get("topics")
        oss.html_url = api_repo_res.get("html_url")
        oss.api_url = api_repo_res.get("url")
        oss.clone_url = api_repo_res.get("clone_url")
        oss.created_at = api_repo_res.get("created_at")
        oss.updated_at = api_repo_res.get("updated_at")

        return oss

    except KeyError as e:
        logger.error("owner's repo data keys have changed, so there was an error converting it to an OSS model", error=e)
        return None

    except Exception as e:
        logger.error("Unknown error parsing github API for owners' details", error=e)
        return None

