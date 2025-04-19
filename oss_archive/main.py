from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy.orm import Session
from scalar_fastapi import get_scalar_api_reference # pyright:ignore[reportMissingTypeStubs]
from typing import Annotated
###
from oss_archive.database.index import lifespan, get_sync_db
from oss_archive.seeders.index import seed as seed_db

from oss_archive.utils.logger import logger

from oss_archive.components.meta_lists.router import router as meta_lists_router
from oss_archive.components.licenses.router import router as licenses_router
from oss_archive.components.meta_items.router import router as meta_items_router
from oss_archive.components.os_softwares.router import router as os_softwares_router


app = FastAPI(
    lifespan=lifespan,
    title="OSS Archive",
    description="OSS Archive is a software built for archiving important Open-Source Software projects, so that it prevent any attempt to lock people access from it.",
    summary="Archiving Open-Source Software project",
    version="0.1.0",
    # docs_url="/docs",
    # redoc_url="/redoc"
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
    compresslevel=5
)

@app.get("/", status_code=status.HTTP_200_OK)
async def homepage():    
    return {
            "title": app.title,
            "description": app.description,
            "version": app.version,
            "documentation_url-1": app.docs_url,
            "documentation_url-2": app.redoc_url,
        }


@app.get(
    "/scalar",
    include_in_schema=False,
    description="Scalar Modern API Client and Reference, check on https://github.com/scalar/scalar"
    )
async def scalar_html() :
    if app.openapi_url is None:
        return "Not Available"

    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

@app.get("/seed", status_code=status.HTTP_200_OK)
def seed(db: Annotated[Session, Depends(dependency=get_sync_db)]):
    try:
        seed_db(db)
        return {"message": "Seedded The Database Successfully"}
    except Exception as e:
        logger.error("Seeding failure", error=e) # pyright: ignore[reportCallIssue]
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Seeding operation has failed")

@app.get("/ping")
async def ping():    
    return {"message": "pong",}


### Adding API routes
app.include_router(meta_lists_router, prefix="/api")
app.include_router(licenses_router, prefix="/api")
app.include_router(meta_items_router, prefix="/api")
app.include_router(os_softwares_router, prefix="/api")
