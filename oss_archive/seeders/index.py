from typing import Annotated, TypedDict
from sqlalchemy.orm import Session, load_only
from sqlalchemy import select, delete, update
from sqlalchemy import exc 
from psycopg import errors
from time import sleep
###
from oss_archive.config import ENV
from oss_archive.utils.logger import logger
# Database
from oss_archive.database.models import MetaList as MetaListModel, MetaItem as MetaItemModel, License, OSSoftware
# Schemas
from oss_archive.schemas import meta_list as MetaListSchemas, meta_item as MetaItemSchemas, os_software as OSSSchemas, license as LicenseSchemas
# JSON
from oss_archive.components.meta_lists.json import get_meta_lists_from_json_files
from oss_archive.components.licenses.json import get_licenses_from_json_file
# Seeders' sources and helplers
from oss_archive.seeders.sources import codeberg
from oss_archive.seeders.helpers import does_license_exists, does_meta_list_exists, get_all_meta_items, get_all_meta_lists


class SeedResults(TypedDict):
    is_meta_lists_seeded: bool
    is_meta_items_seeded: bool
    is_ossoftwares_seeded: bool
    is_licenses_seeded: bool

def seed(db: Session):
    try:
        # 1 - Seeding all Licenses one by one
        # 2 - Seeding all MetaLists one by one
        # 3 - Seeding MetaList's items one by one
        # 4 - Seed MetaItem's Open-Source Softwares one by one

        seed_licenses(db)
        seed_meta_lists(db)
        seed_meta_items(db)
        seed_os_softwares(db)
    except Exception as e:
        logger.error("Error in seed's operations",  error=e)
        return SeedResults(is_meta_lists_seeded=False, is_meta_items_seeded=False, is_ossoftwares_seeded=False, is_licenses_seeded=False)


def seed_meta_lists(db: Session):
    meta_lists: list[MetaListSchemas.JSONSchema] = get_meta_lists_from_json_files()
    for meta_list in meta_lists:
        # Seed JSON MetaList's metadata as a MetaListModel  
        seeded_meta_list = seed_meta_list(meta_list, db)
        if seeded_meta_list is None:
            continue
        # Seed JSON MetaList's items as MetaItemModel
        # for meta_item in meta_list.items:
            # _ = seed_meta_item(meta_item)

def seed_meta_list(meta_list: MetaListSchemas.JSONSchema, db: Session)->MetaListModel | None:
    """Seed Meta list from the meta list's metadata in its json file"""
    try:
        ### Used 2 different conditions block to differntiate the logs.
        if not meta_list.reviewed:
            logger.info(f"Skipped {meta_list.key}'s meta list, because it's not reviewed")
            return None

        meta_list_does_exists = does_meta_list_exists(meta_list.key, db)
        if meta_list_does_exists:
            logger.info(f"Skipped {meta_list.key}'s meta list, because it's already seeded")
            return None

        new_meta_list = MetaListModel()
        new_meta_list.key = meta_list.key
        new_meta_list.name = meta_list.name
        new_meta_list.tags = meta_list.tags
        new_meta_list.priority = meta_list.priority
        new_meta_list.reviewed = meta_list.reviewed


        db.add(new_meta_list)
        db.commit()
        return new_meta_list        

    except errors.UniqueViolation as e:
        db.rollback()
        logger.error(f"Error Inserting meta_list for Unique key Violation, using {meta_list.key} meta_list", meta_list=meta_list, error=e)
        return None
    except errors.CheckViolation as e:
        db.rollback()
        logger.error(f"Error Inserting meta_list for check Violation, using {meta_list.key} meta_list", meta_list=meta_list, error=e)
        return None
    except Exception as e: ## need effective error handling here
        db.rollback()
        logger.error(f"Unknown Error when Inserting meta_list, using {meta_list.key} meta_list", meta_list=meta_list, error=e)
        return None

def seed_meta_items(db: Session):
    meta_lists = get_meta_lists_from_json_files()
    
    for meta_list in meta_lists:
        meta_list_does_exists = does_meta_list_exists(meta_list.key, db)
        if not meta_list_does_exists:
            continue
        for item in meta_list.items:
            _ = seed_meta_item_from_source(meta_list_key=meta_list.key, meta_item=item, db=db)
    return


def seed_meta_item_from_source(meta_list_key: str, meta_item: MetaItemSchemas.JSONSchema, db: Session) -> MetaItemModel | None: #-> Owner:
    match meta_item.source:
        case "github":
            # return github.seed_meta_item(meta_list_key, meta_item, db)
            logger.error("Github OSS source", meta_list_key=meta_list_key, meta_item_owner_username=meta_item.owner_username)
            return None
        case "codeberg":
            return codeberg.seed_meta_item(meta_list_key, meta_item, db)
        # Defualt None value for unknown sources.
        case _:
            logger.error("Unkown OSS source", meta_list_key=meta_list_key, meta_item_owner_username=meta_item.owner_username)
            return None

def seed_os_softwares(db: Session):
    meta_items = get_all_meta_items(db)
    if meta_items is None:
        return
    
    for meta_item in meta_items:
        _ = seed_os_softwares_from_source(meta_item, db)
        # Sleep 0.5 seconds to prevent source's rate-limit
        sleep(0.5)
    return

def seed_os_softwares_from_source(meta_item: MetaItemModel, db: Session): #-> Owner:
    match meta_item.source:
        case "github":
            # return github.seed_meta_item(meta_list_key, meta_item, db)
            logger.error("Github OSS source", meta_item_owner_username=meta_item.owner_username)
            return None
        case "codeberg":
            return codeberg.seed_os_softwares(meta_item, db)
        # Defualt None value for unknown sources.
        case _:
            logger.error("Unkown OSS source", meta_item_owner_username=meta_item.owner_username)
            return None


def seed_licenses(db: Session):
    """Seed Licenses from its JSON file"""
    licenses_data: list[LicenseSchemas.JSONSchema] | None = get_licenses_from_json_file()
    if licenses_data is None:
        raise Exception({'msg': "couldn't get licenses from json file"})
    
    for license_data in licenses_data:
        license_does_exists = does_license_exists(license_data.key, db)
        if license_does_exists:
            continue

        license = License()
        license.key = license_data.key
        license.name = license_data.name
        license.fullname = license_data.fullname
        license.html_url = license_data.html_url
        license.api_url = license_data.api_url

        db.add(license)
        db.commit()

    return
