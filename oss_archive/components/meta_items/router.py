from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exc
from sqlalchemy.orm import joinedload
from uuid import UUID
from typing import Annotated
###
from oss_archive.database.index import get_async_db
from oss_archive.database.models import MetaItem, OSSoftware, MetaList
from oss_archive.components.meta_items import schema

router = APIRouter(tags=["MetaItems"])

@router.get(
    "/meta_items",
    status_code=status.HTTP_200_OK,
    response_model=list[schema.GetMetaItemRes],
    response_model_exclude_none=True
)
async def get_meta_items(db: Annotated[AsyncSession, Depends(get_async_db)]):
    try:
        stmt = select(MetaItem).options(joinedload(MetaItem.meta_list).load_only(MetaList.key, MetaList.name))
        res = await db.scalars(stmt)
        meta_items = res.unique().all()
        return meta_items
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")

@router.get(
    "/meta_items/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schema.GetMetaItemByIDRes,
    response_model_exclude_none=True
)
async def get_meta_item_by_id(id: UUID, db: Annotated[AsyncSession, Depends(get_async_db)]):
    try:
        stmt = select(MetaItem).options(joinedload(MetaItem.meta_list).load_only(MetaList.key, MetaList.name)).options(joinedload(MetaItem.os_softwares).load_only(OSSoftware.id, OSSoftware.name)).where(MetaItem.id == id)

        res = await db.scalars(stmt)
        meta_item = res.unique().one()
        return meta_item
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MetaItem is not found!")
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")

