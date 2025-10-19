from typing import TypedDict
from sqlalchemy.orm import Session
from psycopg import errors
from time import sleep
###
from oss_archive.config import ENV
from oss_archive.database.models import Owner as OwnerModel
from oss_archive.schemas import general as general_schemas
from oss_archive.utils.logger import logger
from oss_archive.seeders import helpers
from oss_archive.seeders.sources import github, codeberg

async def seed():
    ### Make requests to outer APIs async, but the seeding operation can by sync
    # Steps:
    # 1 - Check if categories are seeded into its table
    # 2 - check if owners are seeded into its table

    # 3-  Pull owners and start using each item to seed OSS into oss_table    


    pass


async def seed_owners_oss(db: Session):
    owners = await helpers.get_all_owners(db)
    if owners is None:
        return

    for owner in owners:

        # So that we limit owners seeded while testing.
        if ENV == "dev" and owner.main_category_key not in ["vcs"]:
        # if ENV == "dev" and owner.main_category_key not in ["ai", "prog_awe"]:
            continue
        
        logger.info(f"Owner is in {owner.main_category}")
        _ = await seed_owner_oss_from_source(owner, db)
        # Sleep 0.5 seconds to prevent source's rate-limit
        sleep(0.5)
    return

async def seed_owner_oss_from_source(owner: OwnerModel, db: Session): #-> Owner:
    match owner.source:
        # case "github":
        #     logger.info("Owner is from github")
        #     return await github.seed_owner_oss(owner, db)
        case "codeberg":
            return await codeberg.seed_owner_oss(owner, db)
        # Defualt None value for unknown sources.
        case _:
            logger.error("Unkown OSS source", owner=owner)
            return None
