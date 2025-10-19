from typing import Any, Literal
from subprocess import run, call, CompletedProcess
###
# from oss_archive.config import ARCHIVE_BASE_PATH
from oss_archive.utils.logger import logger
from oss_archive.utils.paths import get_oss_archive_path, does_path_exists, get_absolute_path


async def clone(oss_fullname: str, oss_clone_url: str): #-> tuple[CompletedProcess[bytes], bool]:
    oss_archive_path = get_oss_archive_path(oss_fullname)
    if does_path_exists(oss_archive_path):
        logger.info("OSS Exists, pulling...")
        return await pull(oss_fullname)
    else:
        logger.info("OSS doesn't exists, cloning...")
        result: CompletedProcess[bytes] = run(args=["git", "clone", oss_clone_url, oss_archive_path], capture_output=True)
        if result.returncode != 0:
            logger.error(f"Error when cloning {oss_fullname}", git_result=result, oss_clone_url=oss_clone_url)
            return result, False

        return result, True


## Use git --git-dir="{absolute_path}/.git" to use git pull origin main without navigating to the project folder.
## Example: git --git-dir="/home/m-shrief/Work/Projects/Adeeb_Astro_SSR/.git" pull origin main
async def pull(oss_fullname: str): #-> tuple[CompletedProcess[bytes], Literal[False]] | tuple[CompletedProcess[bytes], bool]:
    oss_archive_path = get_oss_archive_path(oss_fullname)
    oss_archive_abs_path = get_absolute_path(oss_archive_path)

    # result: CompletedProcess[bytes] = run(args=["git", f"--git-dir={oss_archive_abs_path}/.git", "pull", "origin", "--no-recurse-submodules", "main", "master"], capture_output=True)
    result: CompletedProcess[bytes] = run(args=["git", f"--git-dir={oss_archive_abs_path}/.git", "pull", "--all"], capture_output=True)

    if result.returncode != 0:
        logger.error(f"Error when pulling {oss_fullname}", git_result=result)
        return result, False

    return result, True


async def push(oss_fullname: str):
    oss_archive_path = get_oss_archive_path(oss_fullname)
    oss_archive_abs_path = get_absolute_path(oss_archive_path)

    # result: CompletedProcess[bytes] = run(args=["git", f"--git-dir={oss_archive_abs_path}/.git", "push", "origin", "master"], capture_output=True)
    result: CompletedProcess[bytes] = run(args=["git", f"--git-dir={oss_archive_abs_path}/.git", "push", "--all"], capture_output=True)


    if result.returncode != 0:
        logger.error(f"Error when pulling {oss_fullname}", git_result=result)
        return result, False

    return result, True


async def get_info(oss_fullname: str)  -> tuple[dict[str, Any] | None,  bool]:
    oss_archive_path = get_oss_archive_path(oss_fullname)
    oss_archive_abs_path = get_absolute_path(oss_archive_path)

    # result: CompletedProcess[bytes] = run(args=["git", f"--git-dir={oss_archive_abs_path}/.git", "push", "origin", "master"], capture_output=True)
    result: CompletedProcess[bytes] = run(args=["git", "-C", oss_archive_abs_path, "config", "--list"], capture_output=True)


    if result.returncode != 0:
        logger.error(f"Error when pulling {oss_fullname}", git_result=result)
        return None, False


    # Parse the Git config output into a dictionary
    config_dict: dict[str, Any] = {}
    lines = result.stdout.splitlines()
    for line in lines:
        key, value = line.decode().split('=', 1)
        config_dict[key.strip()] = value.strip()

    return config_dict, True
