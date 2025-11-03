from sqlalchemy.orm import Session
from time import sleep
###
from oss_archive.config import ENV
from oss_archive.utils.logger import logger
from oss_archive.database.models import Category as CategoryModel, Owner as OwnerModel, OSS as OSSModel
from oss_archive.database import helpers as db_helpers
from oss_archive.seeders.json import seed_json
from oss_archive.seeders.sources import github as github_source, codeberg as codeberg_source

async def seed(db: Session):
    ### Make requests to outer APIs async, but the seeding operation can by sync
    # Steps:
    # 1 - We seed data in json-archive first to the database
    _ = await seed_json(db)
    # 2 - we should stop the work here if there was no data in the databse, we should atleast check for categories & owners tables.

    # 3-  Pull owners and start using each item to seed OSS into oss_table    

    # 4 - After that we should create "mirrors" user in forgejo if it doesn't exist

    # 5 - Then we begin mirrors OSS while prioritizing the most important one to be done first,
    # and use a method that enable us to resume the work if it was stopped for any reason, and we can use WAL for that. 
    return


async def seed_owners_oss(db: Session):
    owners = await db_helpers.get_all_owners(sync_db=db)
    if owners is None:
        return

    for owner in owners:

        # So that we limit owners seeded while testing.
        if ENV == "dev" and owner.main_category_key not in ["ai", "prog_awe"]:
            continue
        
        logger.info(f"Owner is in {owner.main_category}")
        _ = await seed_owner_oss_from_source(owner, db)
        # Sleep 0.5 seconds to prevent source's rate-limit
        sleep(0.5)
    return

async def seed_owner_oss_from_source(owner: OwnerModel, db: Session): #-> Owner:
    match owner.source:
        case "github":
            return await github_source.seed_owner_oss(owner, db)
        case "codeberg":
            return await codeberg_source.seed_owner_oss(owner, db)
        # Defualt None value for unknown sources.
        case _:
            logger.error("Unkown OSS source", owner=owner)
            return None
