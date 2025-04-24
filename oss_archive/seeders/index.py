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
# from oss_archive.seeders.sources import github
from oss_archive.seeders.helpers import does_license_exists, does_meta_list_exists, does_meta_item_exists, does_oss_exists
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
        
    except Exception as e:
        logger.error("Error in seed's operations",  error=e)
        return SeedResults(is_meta_lists_seeded=False, is_meta_items_seeded=False, is_ossoftwares_seeded=False, is_licenses_seeded=False)



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
