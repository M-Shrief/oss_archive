from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exc
from sqlalchemy.orm import joinedload
from uuid import UUID
from typing import List
###
from oss_archive.database.index import get_db
from oss_archive.database.models import Owner as OwnerModel, OSSoftware, OSSList

from oss_archive.components.owners.schema import Owner as OwnerSchema

router = APIRouter(tags=["Owners"])

@router.get(
    "/owners",
    status_code=status.HTTP_200_OK,
    response_model=List[OwnerSchema],
    response_model_exclude_none=True
)
async def get_owners(db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(OwnerModel).options(joinedload(OwnerModel.oss_list).load_only(OSSList.key, OSSList.name)).options(joinedload(OwnerModel.os_softwares).load_only(OSSoftware.id, OSSoftware.name))
        res = await db.scalars(stmt)
        owners = res.unique().all()
        return owners
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")

@router.get(
    "/owners/{id}",
    status_code=status.HTTP_200_OK,
    response_model=OwnerSchema,
    response_model_exclude_none=True
)
async def get_owner_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(OwnerModel).options(joinedload(OwnerModel.oss_list).load_only(OSSList.key, OSSList.name)).options(joinedload(OwnerModel.os_softwares).load_only(OSSoftware.id, OSSoftware.name)).where(OwnerModel.id == id)
        res = await db.scalars(stmt)
        owner = res.unique().one()
        return owner
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner is not found!")
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")

