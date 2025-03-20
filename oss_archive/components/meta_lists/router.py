from fastapi import APIRouter, HTTPException, status
from typing import List
# from sqlalchemy.ext.asyncio import AsyncSession
###
from oss_archive.components.meta_lists.json import get_meta_lists, get_meta_list_from_file, write_meta_list_file
from oss_archive.components.meta_lists.schema import MetaList, MetaItem


router = APIRouter(tags=["MetaLists"])

@router.get(
    "/meta_lists",
    status_code=status.HTTP_200_OK,
    response_model=List[MetaList],
    response_model_exclude_none=True,
)
async def get_all_meta_lists():
    try:
        meta_lists = get_meta_lists()
        if len(meta_lists) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There's no Meta lists available.")
        return meta_lists
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")

@router.get(
    "/meta_lists/{meta_list_key}",
    status_code=status.HTTP_200_OK,
    response_model=MetaList,
    response_model_exclude_none=True
)
async def get_meta_list(meta_list_key: str):
    try:
        meta_list = get_meta_list_from_file(f"{meta_list_key}.json")
        if meta_list is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta List is not found.")
        return meta_list
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")

@router.post(
    "/meta_lists/{meta_list_key}/add_item",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=MetaList,
    response_model_exclude_none=True
)
async def add_meta_list_item(meta_list_key: str, meta_item: MetaItem):
    try:
        ### Get the meta_list file by key, benefiting from the naming convention we use.
        meta_list_file = f"{meta_list_key}.json"

        meta_list = get_meta_list_from_file(meta_list_file)
        if meta_list is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta List is not found.")

        # mark it as not reviewed to check them before adding it to the database.
        meta_item.reviewed = False
        meta_list.items.append(meta_item)

        is_written = write_meta_list_file(meta_list)
        if not is_written:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error when adding meta item, try again later.")

        meta_list = get_meta_list_from_file(meta_list_file)
        return meta_list

    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")
