from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exc
from sqlalchemy.orm import joinedload, load_only
from uuid import UUID
from typing import List
###
from oss_archive.database.index import get_db
from oss_archive.database.models import OSSoftware as OSSoftwareModel, OSSList, Owner, License

from oss_archive.utils import git, compress

from oss_archive.components.os_softwares.schema import OSSoftware as OSSoftwareSchema

router = APIRouter(tags=["OS_Softwares"])

@router.get(
    "/os_softwares",
    status_code=status.HTTP_200_OK,
    response_model=List[OSSoftwareSchema],
    response_model_exclude_none=True
)
async def get_os_softwares(db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(OSSoftwareModel).options(joinedload(OSSoftwareModel.oss_list).load_only(OSSList.key, OSSList.name)).options(joinedload(OSSoftwareModel.owner).load_only(Owner.id, Owner.username, Owner.name)).options(joinedload(OSSoftwareModel.license).load_only(License.key, License.name))
        res = await db.scalars(statement=stmt)
        os_softwares = res.all()
        return os_softwares
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=F"Unknown error: {e}, try again later")

@router.get(
    "/os_softwares/{id}",
    status_code=status.HTTP_200_OK,
    response_model=OSSoftwareSchema,
    response_model_exclude_none=True
)
async def get_oss_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(OSSoftwareModel).options(joinedload(OSSoftwareModel.oss_list).load_only(OSSList.key, OSSList.name)).options(joinedload(OSSoftwareModel.owner).load_only(Owner.id, Owner.username, Owner.name)).options(joinedload(OSSoftwareModel.license).load_only(License.key, License.name)).where(OSSoftwareModel.id == id)
        res = await db.scalars(statement=stmt)
        oss = res.one()
        return oss
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSS is not found!")
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")


### For testing utilites, most likely we won't expose them in production.
@router.get(
    "/os_softwares/{id}/clone",
    status_code=status.HTTP_200_OK,
    # response_model=OSSoftwareSchema,
    response_model_exclude_none=True
)
async def clone_oss_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(OSSoftwareModel).options(joinedload(OSSoftwareModel.oss_list).load_only(OSSList.key, OSSList.name)).options(joinedload(OSSoftwareModel.owner).load_only(Owner.id, Owner.username, Owner.name)).options(joinedload(OSSoftwareModel.license).load_only(License.key, License.name)).where(OSSoftwareModel.id == id)
        res = await db.scalars(statement=stmt)
        oss: OSSoftwareSchema = res.one()
        # return oss
        res = await git.clone(oss.clone_url, oss.owner.username, oss.name)
        return res
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSS is not found!")
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")


@router.get(
    "/os_softwares/{id}/compress",
    status_code=status.HTTP_200_OK,
    # response_model=OSSoftwareSchema,
    response_model_exclude_none=True
)
async def compress_oss_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(OSSoftwareModel).options(joinedload(OSSoftwareModel.oss_list).load_only(OSSList.key, OSSList.name)).options(joinedload(OSSoftwareModel.owner).load_only(Owner.id, Owner.username, Owner.name)).options(joinedload(OSSoftwareModel.license).load_only(License.key, License.name)).where(OSSoftwareModel.id == id)
        res = await db.scalars(statement=stmt)
        oss: OSSoftwareSchema = res.one()
        # return oss
        await compress.compress(f"{oss.owner.username}:{oss.name}")

        return
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSS is not found!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unknown error: {e}")


@router.get(
    "/os_softwares/{id}/decompress",
    status_code=status.HTTP_200_OK,
    # response_model=OSSoftwareSchema,
    response_model_exclude_none=True
)
async def decompress_oss_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(OSSoftwareModel).options(joinedload(OSSoftwareModel.oss_list).load_only(OSSList.key, OSSList.name)).options(joinedload(OSSoftwareModel.owner).load_only(Owner.id, Owner.username, Owner.name)).options(joinedload(OSSoftwareModel.license).load_only(License.key, License.name)).where(OSSoftwareModel.id == id)
        res = await db.scalars(statement=stmt)
        oss: OSSoftwareSchema = res.one()
        # return oss
        path = f"{oss.owner.username}:{oss.name}.tar"
        await compress.decompress(path)

        return
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSS is not found!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unknown error: {e}")