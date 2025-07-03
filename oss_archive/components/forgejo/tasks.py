from httpx import Timeout
###
from oss_archive.components.forgejo import requests
from oss_archive.components.forgejo.schema import ForgejoRepo, MigrateRepoReqBody
from oss_archive.utils.logger import logger


async def migrate_repo_task(body: MigrateRepoReqBody):
    logger.info("Migrating repo...", repo=f"{body.repo_owner}/{body.repo_name}", source=body.clone_addr)
    result = await requests.async_post(
        endpoint="/repos/migrate",
        body=body.model_dump(),
        timeout=Timeout(timeout=500.0, connect=100.0)
        )
    if result is None:
        logger.error("Migrating error", result="result is Noen")
        return

    new_repo: ForgejoRepo = result.json()
    logger.info("Mirrored repo correctly", repo=f"{body.repo_owner}/{body.repo_name}", source=body.clone_addr)
    return new_repo 