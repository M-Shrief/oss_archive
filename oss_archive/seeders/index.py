from typing import List
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
### 
from oss_archive.config import ENV
from oss_archive.utils.logger import logger
from oss_archive.database.models import Owner, OSSList, License, OSSoftware

from oss_archive.components.meta_lists.json import get_meta_lists, get_meta_list_from_file, write_meta_list_file
from oss_archive.components.meta_lists.schema import MetaList, MetaItem

from oss_archive.components.licenses.json import get_licenses_from_json_file

from oss_archive.seeders.sources import codeberg, github



def seed(db: Session):
    seed_oss_list(db)
    seed_licenses(db)
    seed_owners_and_their_repos(db)
    return


def seed_oss_list(db: Session):
    meta_lists: List[MetaList] = get_meta_lists()
    try:
        oss_lists: List[OSSList] = []
        for meta_list in meta_lists:   
            if not meta_list.reviewed:
                logger.info(f"Skipped {meta_list.key}'s meta list, because it's not reviewed")
                continue
            if meta_list.is_seeded:
                logger.info(f"Skipped {meta_list.key}'s meta list, because it's seeded")
                continue
            
            oss_list = OSSList()

            oss_list.key = meta_list.key
            oss_list.name = meta_list.name
            oss_list.tags = meta_list.tags
            oss_list.priority = meta_list.priority
            oss_list.reviewed = meta_list.reviewed

            oss_lists.append(oss_list)

        db.add_all(oss_lists)
        db.commit()

        ### if all was commited to the database successfully, then mark each meta_list.is_seeded = True
        for meta_list in meta_lists:
            meta_list.is_seeded = True
            is_written = write_meta_list_file(meta_list)
            if not is_written:
                stmt = delete(OSSList).where(OSSList.key == meta_list.key)
                db.execute(statement=stmt)
                db.commit()

        return 
    except Exception as e:
        logger.error("Error while seeding oss_lists", error=e)
        return None

def seed_licenses(db: Session):
    licenses: List[License] = []

    licenses_data = get_licenses_from_json_file()
    if licenses_data is None:
        raise Exception({'msg': "couldn't get licenses from json file"})
    for item in licenses_data:
        lic = License()
        lic.key = item.key
        lic.name = item.name
        lic.fullname = item.fullname
        lic.html_url = item.html_url
        lic.api_url = item.api_url

        licenses.append(lic)

    db.add_all(licenses)
    db.commit()
    return


def seed_owners_and_their_repos(db: Session): # , oss_lists_items: List[Owner]
    res = db.scalars(statement=select(OSSList))
    all_oss_lists: List[OSSList] = res.all()

    reviewed_oss_lists: List[OSSList] = [oss_list for oss_list in all_oss_lists if oss_list.reviewed]
    for oss_list in reviewed_oss_lists:
        if ENV == "dev" and oss_list.key not in ["ai", "prog_web"]:
            continue
        logger.info(f"seeding {oss_list.key} oss_list")
        meta_list = get_meta_list_from_file(f"{oss_list.key}.json")
        for item in meta_list.items:
            __add_meta_item(oss_list.key, item, db)
    
    return

def __add_meta_item(meta_list_key: str, meta_item: MetaItem, db: Session) -> (Owner | None, List[OSSoftware] | None): #-> Owner:
    if not meta_item.reviewed: ### Not adding meta items untill it's reviewed.
        return None, None 
    match meta_item.source:
        case "github":
            return github.add_meta_item(meta_list_key, meta_item, db)
        case "codeberg":
            return codeberg.add_meta_item(meta_list_key, meta_item, db)
        # Defualt None value for unknown sources.
        case _:
            logger.error("Unkown OSS source", meta_list_key=meta_list_key, meta_item=meta_item)
            return None, None





### Old Async Implementation ##################

# from typing import List
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from sqlalchemy.orm import joinedload
# from requests import get
# ### 
# from oss_archive.config import ENV
# from oss_archive.utils.logger import logger
# from oss_archive.database.models import Owner, OSSList, License, OSSoftware

# from oss_archive.components.meta_lists.utils import get_meta_lists, get_meta_list_from_file
# from oss_archive.components.meta_lists.schema import MetaList, MetaItem

# from oss_archive.seeders.sources.github import get_meta_list_item_from_github, get_owner_repos
# from oss_archive.seeders.sources.codeberg import add_meta_item



# async def seed(db: AsyncSession):
#     ### New
#     # await seed_oss_list(db)
#     # await seed_licenses(db)
#     await seed_owners_and_their_repos(db)
#     # await seed_repos(db)

#     ### Old
#     # meta_lists : List[MetaList] = get_meta_lists()
#     # new_meta_lists = await seed_oss_list(db, meta_lists)
#     # if new_meta_lists is None:
#     #     return
#     # meta_lists_items: List[Owner] = []
#     # for meta_list in meta_lists:
#     #     ## Limit seeding operations to one  in Development to one oss_list
#     #     if ENV == "dev" and meta_list.key != "ai":
#     #         continue
#     #     for item in meta_list.items:
#     #         data = await __get_meta_list_item(meta_list.key, item)
#     #         if data is None:
#     #             continue
#     #         meta_lists_items.append(data)
    
#     # await seed_owners(db, meta_lists_items)
#     # await seed_licenses(db)
#     # await seed_repos(db)
#     return


# async def seed_oss_list(db: AsyncSession):
#     meta_lists: List[MetaList] = get_meta_lists()
#     try:
#         new_lists: List[OSSList] = []
#         for item in meta_lists:
#             oss_list = OSSList()

#             oss_list.key = item.key
#             oss_list.name = item.name
#             oss_list.tags = item.tags
#             oss_list.priority = item.priority
#             oss_list.reviewed = item.reviewed

#             new_lists.append(oss_list)
        
#         db.add_all(new_lists)
#         await db.commit()

#         return 
#     except Exception as e:
#         logger.error("Error while seeding oss_lists", error=e)
#         return None

# async def seed_licenses(db: AsyncSession):
#     licenses_res = get(url="https://api.github.com/licenses")
#     if licenses_res.status_code != 200:
#         return None
#     licenses_arr: [] = licenses_res.json()

#     licenses: List[License] = []

#     for item in licenses_arr:
#         license_res = get(item["url"])
#         if license_res.status_code != 200:
#             return None
#         license_json: [] = license_res.json()

#         lic = License()

#         lic.key = license_json["key"]
#         lic.name = license_json["name"]
#         lic.html_url = license_json["html_url"]
#         lic.api_url = license_json["url"]

#         licenses.append(lic)
    
#     db.add_all(licenses)
#     await db.commit()
#     return


# async def seed_owners_and_their_repos(db: AsyncSession): # , oss_lists_items: List[Owner]
#     # Get all OSSLists in the database
#     res = await db.scalars(statement=select(OSSList))
#     all_oss_lists: List[OSSList] = res.all()

#     reviewed_oss_lists: List[OSSList] = [oss_list for oss_list in all_oss_lists if oss_list.reviewed]
#     # oss_lists_owners: List[Owner] = []
#     for oss_list in reviewed_oss_lists:
#         ## Limit seeding operations in development to one oss_list
#         # logger.info("oss_list", oss_list=oss_list.key)
#         if ENV == "dev" and oss_list.key != "web":
#             continue
#         ### get the respective meta_list for oss_list
#         meta_list = get_meta_list_from_file(f"{oss_list.key}.json")
#         for item in meta_list.items:
#             # logger.info("Got Meta Item", oss_list_key=oss_list.key, meta_item=item)
#             await __get_meta_list_item(oss_list.key, item, db)
#     #         if owner is None:
#     #             continue
#     #         oss_lists_owners.append(owner)

#     # db.add_all(oss_lists_owners)
#     # await db.commit()
#     return

# # async def seed_repos(db: AsyncSession):
# #     stmt = select(OSSList).options(joinedload(OSSList.owners))
# #     res = await db.scalars(statement=stmt)
# #     oss_lists: List[OSSList] = res.unique().all() 

# #     for oss_list in oss_lists:
# #         for owner in oss_list.owners:
# #             oss_arr_from_owner_repos = await get_owner_repos(oss_list.key, owner)
# #             if oss_arr_from_owner_repos is None:
# #                 continue
# #             db.add_all(oss_arr_from_owner_repos)
# #             # await db.commit()
    
# #     await db.commit()

# #     return

# async def __get_meta_list_item(meta_list_key: str, meta_item: MetaItem, db: AsyncSession) -> (Owner | None, List[OSSoftware] | None): #-> Owner:
#     match meta_item.source:
#         case "github":
#             return await get_meta_list_item_from_github(meta_list_key, meta_item)
#         case "codeberg":
#             return await add_meta_item(meta_list_key, meta_item, db)
#         # Defualt None value for unknown sources.
#         case _:
#             logger.error("Unkown OSS source", meta_list_key=meta_list_key, meta_item=meta_item)
#             return None

