from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exc
from sqlalchemy.orm import joinedload, load_only
from typing import List
# from pydantic import BaseModel
###
from oss_archive.database.index import get_db
from oss_archive.database.models import OSSList as OSSListModel, Owner, OSSoftware

from oss_archive.components.oss_lists.schema import OSSList as OSSListSchema

router = APIRouter(tags=["OSSLists"])

@router.get(
    "/oss_lists",
    status_code=status.HTTP_200_OK,
    response_model=List[OSSListSchema],
    response_model_exclude_none=True
)
async def get_oss_lists(db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(OSSListModel).options(joinedload(OSSListModel.owners).load_only(Owner.id, Owner.username, Owner.name)).options(joinedload(OSSListModel.os_softwares).load_only(OSSoftware.id, OSSoftware.name)) #.offset().limit()
        res = await db.scalars(statement=stmt)
        oss_lists = res.unique().all()
        if len(oss_lists) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There's no Meta lists available.")
        return oss_lists
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unknown error: {e}, try again later")

@router.get(
    "/oss_lists/{key}",
    status_code=status.HTTP_200_OK,
    response_model=OSSListSchema,
    response_model_exclude_none=True
)
async def get_oss_list(key: str, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(OSSListModel).options(joinedload(OSSListModel.owners).load_only(Owner.id, Owner.username, Owner.name)).options(joinedload(OSSListModel.os_softwares).load_only(OSSoftware.id, OSSoftware.name, OSSoftware.description)).where(OSSListModel.key == key)
        res = await db.scalars(statement=stmt)
        oss_list = res.unique().one()
        return oss_list
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSS List is not found!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=F"Unknown error: {e}",)


# @router.post(
#     "/oss_lists"
# )
# async def add_new_oss_list():
#     pass

# @router.put(
#     "/oss_lists/{oss_list_key}"
# )
# async def update_oss_list(db: AsyncSession = Depends(get_db)):
#     pass