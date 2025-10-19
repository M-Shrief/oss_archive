from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exc, delete, func
from typing import Annotated
###
from oss_archive.utils.logger import logger
from oss_archive.database.index import get_async_db
from oss_archive.database.models import Category as CategoryModel
from oss_archive.seeders.helpers import does_category_exists
from oss_archive.schemas import category as category_schemas, api as api_schemas
from oss_archive.components.categories import schema as component_schemas #, json as component_json

router = APIRouter(tags=["Categories"])

@router.get(
    "/categories",
    status_code=status.HTTP_200_OK,
    response_model=api_schemas.GetAll_Res[category_schemas.DescriptiveSchema],
    response_model_exclude_none=True,
)
async def get_categories(queries: Annotated[api_schemas.SharedQueriesForGetAllRequests, Query()], db: Annotated[AsyncSession, Depends(get_async_db)]):
    try: #
        stmt = select(CategoryModel).offset(queries.offset).limit(queries.limit)
        resp  = await db.scalars(statement=stmt)
        result = resp.all()
        categories: list[category_schemas.DescriptiveSchema] =  [category_schemas.DescriptiveSchema.model_validate(item, from_attributes=True) for item in list(result)]

        count_resp = await db.execute(select(func.count()).select_from(CategoryModel))
        count =  count_resp.scalar()

        return api_schemas.GetAll_Res[category_schemas.DescriptiveSchema](data=categories, offset=queries.offset, limit=queries.limit, total_count=count)

    except Exception as e:
        logger.error("Error when getting categories", error=e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")


@router.get(
    "/categories/{key}",
    status_code=status.HTTP_200_OK,
    response_model=component_schemas.GetCategoryByKey_Res,
    response_model_exclude_none=True
)
async def get_category_by_key(key: str, db: Annotated[AsyncSession, Depends(get_async_db)]):
    try:
        stmt = select(CategoryModel).where(CategoryModel.key == key)
        res = await db.scalars(statement=stmt)
        category = res.unique().one()
        return category
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category is not found!")
    except Exception as e:
        logger.error("Error when getting a category by key", error=e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")

@router.post(
    path="/categories/",
    status_code=status.HTTP_201_CREATED,
    response_model=component_schemas.CreateCategory_Res,
    response_model_exclude_none=True
)
async def create_category(category: component_schemas.CreateCategory_Req, db: Annotated[AsyncSession, Depends(get_async_db)]):
    try:
        new_category = CategoryModel(**category.model_dump())
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)

        return new_category

    except Exception as e:
        logger.error("Error occurred while creating a category", error=e)
        await db.rollback()
        if "psycopg.errors.UniqueViolation" in str(e):
            detail_msg = "Category does already exists"
            raise HTTPException(status.HTTP_409_CONFLICT, detail=detail_msg)
        else:
            detail_msg = "An error occurred while creating a category, try again later."
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=detail_msg)

@router.post(
    path="/categories/many",
    status_code=status.HTTP_201_CREATED,
    response_model=component_schemas.CreateCategories_Res,
    response_model_exclude_none=True
)
async def create_categories(req_body: component_schemas.CreateCategories_Req, db: Annotated[AsyncSession, Depends(get_async_db)]):
    try:
        new_categories: list[category_schemas.FullSchema] = []
        already_exists: list[str] = []

        for category in req_body.categories:
            does_exist = await does_category_exists(category.key, db)
            if does_exist:
                already_exists.append(category.key)
                continue
            else:
                new_category = CategoryModel(**category.model_dump())        
                _ = db.add(new_category)
                await db.commit()
                await db.refresh(new_category)
                new_categories.append(category_schemas.FullSchema.model_validate(new_category, from_attributes=True))

        return component_schemas.CreateCategories_Res(
            new_categories=new_categories,
            already_exists=already_exists,
        )

    except Exception as e:
        logger.error("Error occurred while creating a categories", error=e)
        detail_msg = "An error occurred while creating a categories, try again later."
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=detail_msg)


@router.put(
    "/categories/{key}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=api_schemas.Update_Res,
    response_model_exclude_none=True
)
async def update_one(key: str, req_body: component_schemas.Update_Req, db: Annotated[AsyncSession, Depends(get_async_db)]):
    try:
        stmt = select(CategoryModel).where(CategoryModel.key == key)
        res = await db.scalars(statement=stmt)    
        existing_category = res.unique().one()

        new_category_data = req_body.model_dump(exclude_none=True)  # Exclude None fields from the request body

        for key, value in new_category_data.items():
            setattr(existing_category, key, value)

        await db.commit()
        return api_schemas.Update_Res()
        
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category is not found!")
    except Exception as e:
        logger.error("Error when updating category", error=e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")


@router.delete(
    "/categories/{key}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=api_schemas.Delete_Res,
    response_model_exclude_none=True
)
async def delete_one(key: str, db: Annotated[AsyncSession, Depends(get_async_db)]):
    try:
        stmt = delete(CategoryModel).where(CategoryModel.key == key)
        _ = await db.execute(statement=stmt)
        await db.commit()

        return api_schemas.Delete_Res()
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category is not found!")
    except Exception as e:
        logger.error("Error when deleting category", error=e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")
