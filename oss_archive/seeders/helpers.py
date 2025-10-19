from sqlalchemy.orm import Session
from sqlalchemy import select, exc 
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Annotated
from collections.abc import Sequence
### 
from oss_archive.utils.logger import logger
from oss_archive.database.models import OSS as OSSModel, Owner as OwnerModel, Category as CategoryModel
from oss_archive.schemas.general import ActionsEnum

def should_apply_action_on_oss(owner: OwnerModel, repo_name: str | None)-> bool:
    """Decide should we apply the owner.actions on the OSS or not."""
    if repo_name is None:
        return False

    should_download = False
    # Filter seeded repos depending on meta_item.actions && meta_item.actions_on
    match owner.actions:
        case ActionsEnum.ArchiveAll: # Get all repos without filtering
            should_download = True
        case ActionsEnum.ArchiveOnly:
            if repo_name in owner.actions_on:
                should_download = True
        case ActionsEnum.ArchiveAllExcept:
            if repo_name not in owner.actions_on:
                should_download = True
    
    return should_download


async def get_all_owners(db: Session) -> Sequence[OwnerModel] | None:
    try:
        stmt = select(OwnerModel)
        res = db.scalars(stmt)
        owners = res.all()
        logger.info("Got owners", length=len(owners))
        return owners
    except Exception as e:
        logger.error("Unknown error getting all owners", error=e)
        return None


async def does_category_exists(category_key: str, db: AsyncSession |  Session) -> bool | None:
    """check if category exists, if result is None then there was unknown error."""
    try:
        if type(db) is AsyncSession:
            stmt = select(CategoryModel).where(CategoryModel.key == category_key)
            res = await db.scalars(statement=stmt)

            _ = res.one() # if it exists in won't raise an error
            return True
        elif type(db) is Session:
            stmt = select(CategoryModel).where(CategoryModel.key == category_key)
            res = db.scalars(statement=stmt)

            _ = res.one() # if it exists in won't raise an error
            return True
    except exc.NoResultFound:
        return False
    except Exception:
        return None

async def does_owner_exists(owner_username: str, db: AsyncSession |  Session) -> bool | None:
    """check if owner exists, if result is None then there was unknown error."""
    try:
        if type(db) is AsyncSession:
            stmt = select(OwnerModel).where(OwnerModel.username == owner_username)
            res = await db.scalars(statement=stmt)

            _ = res.one() # if it exists in won't raise an error
            return True
        elif type(db) is Session:
            stmt = select(OwnerModel).where(OwnerModel.username == owner_username)
            res = db.scalars(statement=stmt)

            _ = res.one() # if it exists in won't raise an error
            return True
    except exc.NoResultFound:
        return False
    except Exception:
        return None

async def does_oss_exists(oss_fullname: str, db: AsyncSession |  Session) -> bool | None:
    """check if OSS exists, if result is None then there was unknown error."""
    try:
        if type(db) is AsyncSession:
            stmt = select(OSSModel).where(OSSModel.fullname == oss_fullname)
            res = await db.scalars(statement=stmt)

            _ = res.one() # if it exists in won't raise an error
            return True
        elif type(db) is Session:
            stmt = select(OSSModel).where(OSSModel.fullname == oss_fullname)
            res = db.scalars(statement=stmt)

            _ = res.one() # if it exists in won't raise an error
            return True
    except exc.NoResultFound:
        return False
    except Exception:
        return None
