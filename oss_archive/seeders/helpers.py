from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import exc 
from typing import Any
from collections.abc import Sequence
### 
from oss_archive.utils.logger import logger
from oss_archive.database.models import MetaList, MetaItem, OSSoftware, License
from oss_archive.schemas.general import ActionsType

def get_all_meta_lists(db: Session) -> Sequence[MetaList] | None:
    try:
        stmt = select(MetaList)
        res = db.scalars(stmt)
        meta_lists = res.all()
        return meta_lists
    except Exception as e:
        logger.error("Unknown error getting all meta lists", error=e)
        return None


def get_all_meta_items(db: Session) -> Sequence[MetaItem] | None:
    try:
        stmt = select(MetaItem)
        res = db.scalars(stmt)
        meta_items = res.all()
        return meta_items
    except Exception as e:
        logger.error("Unknown error getting all meta items", error=e)
        return None


def should_apply_action_on_oss(meta_item: MetaItem, repo_dict: dict[str, Any])-> bool:
    """Decide should we apply the meta_item.actions on the OSS or not."""
    should_download = False
    repo_name: str | Any = repo_dict.get("name")
    if repo_name is None:
        return False

    # Filter seeded repos depending on meta_item.actions && meta_item.actions_on
    match meta_item.actions:
        case ActionsType.ArchiveAll: # Get all repos without filtering
            should_download = True
        case ActionsType.ArchiveOnly:
            if repo_name in meta_item.actions_on:
                should_download = True
        case ActionsType.ArchiveExcept:
            if repo_name not in meta_item.actions_on:
                should_download = True
    
    return should_download


def does_meta_list_exists(meta_list_key: str, db: Session) -> bool:
    try:
        stmt = select(MetaList).where(MetaList.key == meta_list_key)
        res = db.scalars(statement=stmt)

        _ = res.one() # if it exists in won't raise an error
        return True
    except exc.NoResultFound:
        return False

def does_meta_item_exists(meta_item_owner_username: str, db: Session) -> bool:
    try:
        stmt = select(MetaItem).where(MetaItem.owner_username == meta_item_owner_username)
        res = db.scalars(statement=stmt)

        _ = res.one() # if it exists in won't raise an error
        return True
    except exc.NoResultFound:
        return False

def does_oss_exists(oss_fullname: str, db: Session) -> bool:
    try:
        stmt = select(OSSoftware).where(OSSoftware.fullname == oss_fullname)
        res = db.scalars(statement=stmt)

        _ = res.one() # if it exists in won't raise an error
        return True
    except exc.NoResultFound:
        return False

def does_license_exists(license_key: str, db: Session) -> bool:
    try:
        stmt = select(License).where(License.key == license_key)
        res = db.scalars(statement=stmt)

        _ = res.one() # if it exists in won't raise an error
        return True
    except exc.NoResultFound:
        return False
