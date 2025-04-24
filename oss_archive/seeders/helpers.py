from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import exc 
from uuid import UUID
from collections.abc import Sequence
### 
from oss_archive.utils.logger import logger
from oss_archive.database.models import MetaList, MetaItem, OSSoftware, License

def get_all_meta_items(db: Session) -> Sequence[MetaItem] | None:
    try:
        stmt = select(MetaItem)
        res = db.scalars(stmt)
        meta_items = res.all()
        return meta_items
    except Exception as e:
        logger.error("Unknown error getting all meta_items", error=e)
        return None


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
