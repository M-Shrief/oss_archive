from httpx import Timeout
###
from oss_archive.config import Forgejo
from oss_archive.utils import httpx
from oss_archive.utils.logger import logger
from oss_archive.components.forgejo.schema import ForgejoRepo, MigrateRepoReqBody
from oss_archive.components.forgejo.shared import base_headers


async def migrate_repo_task(repo_data: MigrateRepoReqBody):
    logger.info("Migrating repo...", repo=f"{repo_data.repo_owner}/{repo_data.repo_name}", source=repo_data.clone_addr)

    result = await httpx.async_post(
        base_url=Forgejo.get("base_url") or "",
        endpoint="/repos/migrate",
        body=repo_data.model_dump(),
        headers=base_headers,
        timeout=Timeout(timeout=500.0, connect=100.0)
        )

    if result is None:
        logger.error("Migrating error", result="result is Noen")
        return

    new_repo: ForgejoRepo = result.json()
    logger.info("Mirrored repo correctly", repo=f"{repo_data.repo_owner}/{repo_data.repo_name}", source=repo_data.clone_addr)
    return new_repo 