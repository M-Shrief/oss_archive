from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exc
from sqlalchemy.orm import joinedload, load_only
from typing import Annotated
# from sqlalchemy.ext.asyncio import AsyncSession
###
from oss_archive.database.index import get_async_db
from oss_archive.database.models import MetaItem, MetaList as MetaListModel
from oss_archive.components.meta_lists import schema
from oss_archive.components.meta_lists.json import get_meta_list_from_file, write_meta_list_file


router = APIRouter(tags=["MetaLists"])

@router.get(
    "/meta_lists",
    status_code=status.HTTP_200_OK,
    response_model=list[schema.GetAllMetaListsItemRes],
    response_model_exclude_none=True,
)
async def get_all_meta_lists(db: Annotated[AsyncSession, Depends(get_async_db)]):
    try:
        stmt = select(MetaListModel)#.offset().limit()
        res = await db.scalars(statement=stmt)
        meta_lists = res.all()
        if len(meta_lists) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There's no Meta lists available.")
        return meta_lists
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")


@router.get(
    "/meta_lists/{meta_list_key}",
    status_code=status.HTTP_200_OK,
    response_model=schema.GetMetaListByKey,
    response_model_exclude_none=True
)
async def get_meta_list(meta_list_key: str, db: Annotated[AsyncSession, Depends(get_async_db)]):
    try:
        stmt = select(MetaListModel).options(joinedload(MetaListModel.meta_items).load_only(MetaItem.id, MetaItem.owner_username, MetaItem.source)).where(MetaListModel.key == meta_list_key)
        res = await db.scalars(statement=stmt)
        meta_list = res.unique().one()
        return meta_list
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSS List is not found!")
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")

# @router.get(
#     "/meta_lists/{meta_list_key}/json",
#     status_code=status.HTTP_200_OK,
#     # response_model=MetaListSchema,
#     response_model_exclude_none=True
# )
# async def get_meta_list_json_file(meta_list_key: str):
#     try:
#         meta_list = get_meta_list_from_file(f"{meta_list_key}.json")
#         if meta_list is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta List is not found.")
#         return meta_list
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")


# @router.post(
#     "/meta_lists/{meta_list_key}/add_item",
#     status_code=status.HTTP_202_ACCEPTED,
#     # response_model=MetaListSchema,
#     response_model_exclude_none=True
# )
# async def add_meta_list_item(meta_list_key: str, meta_item):
#     try:
#         ### Get the meta_list file by key, benefiting from the naming convention we use.
#         meta_list_file = f"{meta_list_key}.json"

#         meta_list = get_meta_list_from_file(meta_list_file)
#         if meta_list is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta List is not found.")

#         # mark it as not reviewed to check them before adding it to the database.
#         meta_item.reviewed = False
#         meta_list.items.append(meta_item)

#         is_written = write_meta_list_file(meta_list)
#         if not is_written:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error when adding meta item, try again later.")

#         meta_list = get_meta_list_from_file(meta_list_file)
#         return meta_list

#     except Exception:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")
