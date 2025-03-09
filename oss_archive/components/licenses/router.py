from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exc
###
from oss_archive.database.index import get_db
from oss_archive.database.models import License as LicenseModel
from oss_archive.components.licenses.schema import License as LicenseSchema 

router = APIRouter(tags=["Licenses"])

@router.get(
    "/licenses",
    status_code=status.HTTP_200_OK,
    response_model=List[LicenseSchema],
    response_model_exclude_none=True
)
async def get_licenses(db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(LicenseModel)
        res = await db.scalars(statement=stmt)

        licenses = res.all()
        return licenses
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")

@router.get(
    "/licenses/{key}",
    status_code=status.HTTP_200_OK,
    response_model=LicenseSchema,
    response_model_exclude_none=True
)
async def get_license_by_key(key: str, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(LicenseModel).where(LicenseModel.key == key)
        res = await db.scalars(statement=stmt)

        license = res.one()
        return license
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License is not found!")
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error, try again later")