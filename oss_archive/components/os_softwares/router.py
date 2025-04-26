from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exc
from sqlalchemy.orm import joinedload, load_only
from uuid import UUID
from typing import Annotated
###
from oss_archive.database.index import get_async_db
from oss_archive.database.models import OSSoftware as OSSoftwareModel, MetaList, MetaItem, License
from oss_archive.components.os_softwares import schema 
# from oss_archive.utils import git, tarfile

router = APIRouter(tags=["OS_Softwares"])

@router.get(
    "/os_softwares",
    status_code=status.HTTP_200_OK,
    response_model=list[schema.GetOSSoftwaresItemRes],
    response_model_exclude_none=True
)
async def get_os_softwares(db: Annotated[AsyncSession, Depends(get_async_db)]):
    try:
        stmt = select(OSSoftwareModel).options(joinedload(OSSoftwareModel.meta_list).load_only(MetaList.key, MetaList.name)).options(joinedload(OSSoftwareModel.meta_item).load_only(MetaItem.id, MetaItem.owner_username, MetaItem.source)).options(joinedload(OSSoftwareModel.license).load_only(License.key, License.name))
        res = await db.scalars(statement=stmt)
        os_softwares = res.all()
        return os_softwares
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=F"Unknown error: {e}, try again later")

@router.get(
    "/os_softwares/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schema.GetOSSoftwareByIDRes,
    response_model_exclude_none=True
)
async def get_oss_by_id(id: UUID, db: Annotated[AsyncSession, Depends(get_async_db)]):
    try:
        stmt = select(OSSoftwareModel).options(joinedload(OSSoftwareModel.meta_list).load_only(MetaList.key, MetaList.name)).options(joinedload(OSSoftwareModel.meta_item).load_only(MetaItem.id, MetaItem.owner_username, MetaItem.source)).options(joinedload(OSSoftwareModel.license).load_only(License.key, License.name)).where(OSSoftwareModel.id == id)
        res = await db.scalars(statement=stmt)
        oss = res.one()
        return oss
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSS is not found!")
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")


### For testing utilites, most likely we won't expose them in production.
# @router.get(
#     "/os_softwares/{id}/clone",
#     status_code=status.HTTP_200_OK,
#     # response_model=OSSoftwareSchema,
#     response_model_exclude_none=True
# )
# async def clone_oss_by_id(id: UUID, db: Annotated[AsyncSession, Depends(get_async_db)]):
#     try:
#         stmt = select(OSSoftwareModel).options(joinedload(OSSoftwareModel.meta_list).load_only(MetaList.key, MetaList.name)).options(joinedload(OSSoftwareModel.meta_item).load_only(MetaItem.id, MetaItem.owner_username, MetaItem.owner_name, MetaItem.owner_type)).options(joinedload(OSSoftwareModel.license).load_only(License.key, License.name)).where(OSSoftwareModel.id == id)
#         res = await db.scalars(statement=stmt)
#         oss: OSSoftwareModel = res.one()
#         # return oss
#         if oss.clone_url is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSS's clone url is not found!")
#         res, iscloned = await git.clone(oss.clone_url, oss.meta_item.owner_username, oss.name)
        
#         if iscloned:
#             return {"message": "Clone operation is successfull."}
#         else:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Operation have failed, try again later")
#     except exc.NoResultFound:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSS is not found!")
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")


# @router.get(
#     "/os_softwares/{id}/compress",
#     status_code=status.HTTP_200_OK,
#     # response_model=OSSoftwareSchema,
#     response_model_exclude_none=True
# )
# async def compress_oss_by_id(id: UUID, db: Annotated[AsyncSession, Depends(get_async_db)]):
#     try:
#         stmt = select(OSSoftwareModel).options(joinedload(OSSoftwareModel.meta_list).load_only(MetaList.key, MetaList.name)).options(joinedload(OSSoftwareModel.meta_item).load_only(MetaItem.id, MetaItem.owner_username, MetaItem.owner_name, MetaItem.owner_type)).options(joinedload(OSSoftwareModel.license).load_only(License.key, License.name)).where(OSSoftwareModel.id == id)
#         res = await db.scalars(statement=stmt)
#         oss: OSSoftwareModel = res.one()
        
#         iscompressed = await tarfile.compress(oss.fullname)
#         if iscompressed:
#             return {"message": "Operation Succeded, OSS have been compressed"}
#         else:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Operation have failed, try again later")
#     except exc.NoResultFound:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSS is not found!")
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unknown error: {e}")


# @router.get(
#     "/os_softwares/{id}/decompress",
#     status_code=status.HTTP_200_OK,
#     # response_model=OSSoftwareSchema,
#     response_model_exclude_none=True
# )
# async def decompress_oss_by_id(id: UUID, db: Annotated[AsyncSession, Depends(get_async_db)]):
#     try:
#         stmt = select(OSSoftwareModel).options(joinedload(OSSoftwareModel.meta_list).load_only(MetaList.key, MetaList.name)).options(joinedload(OSSoftwareModel.meta_item).load_only(MetaItem.id, MetaItem.owner_username, MetaItem.owner_name, MetaItem.owner_type)).options(joinedload(OSSoftwareModel.license).load_only(License.key, License.name)).where(OSSoftwareModel.id == id)
#         res = await db.scalars(statement=stmt)
#         oss: OSSoftwareModel = res.one()

#         isdecompressed = await tarfile.decompress(oss.fullname)
#         if isdecompressed:
#             return {"message": "Operation Succeded, OSS have been decompressed"}
#         else:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Operation have failed, try again later")

#     except exc.NoResultFound:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSS is not found!")
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unknown error: {e}")