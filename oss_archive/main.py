from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
###
from oss_archive.database.index import lifespan, get_db, get_sync_db
from oss_archive.seeders.index import seed as seed_db

from oss_archive.components.meta_lists.router import router as meta_lists_router
from oss_archive.components.oss_lists.router import router as oss_lists_router
from oss_archive.components.licenses.router import router as licenses_router
from oss_archive.components.os_softwares.router import router as os_softwares_router
from oss_archive.components.owners.router import router as owners_router


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

@app.get("/seed", status_code=status.HTTP_200_OK)
def seed(db: Session = Depends(get_sync_db)):    
    seed_db(db)
    return {"message": "Seedded The Database Successfully"}

@app.get("/ping")
async def ping():    
    return {"message": "pong",}


### Adding API routes
app.include_router(meta_lists_router, prefix="/api")
app.include_router(oss_lists_router, prefix="/api")
app.include_router(licenses_router, prefix="/api")
app.include_router(owners_router, prefix="/api")
app.include_router(os_softwares_router, prefix="/api")
