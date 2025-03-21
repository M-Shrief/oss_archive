from enum import Enum
from subprocess import run, call, CompletedProcess
###
from oss_archive.config import ARCHIVE_BASE_PATH
from oss_archive.utils.logger import logger


async def clone(clone_url: str, owner_username: str, repo_name: str)->CompletedProcess:
    result = run(["git", "clone", clone_url, f"{ARCHIVE_BASE_PATH}/{owner_username}:{repo_name}"], capture_output=True)
    # res.stderr
    match result.returncode:
        case 0:
            ### Return as a success
            logger.info("Successful Clone Operation", clone_url=clone_url)
            return result
        # case 1:
        #     logger.error("Git Clone error", result=result)
        case _:
            logger.error("Git Clone Uknownerror",result=result)
        
    return result


async def push():
    pass

# class ReturnCodes(Enum):
#     Success = 0
#     Err_Unfinished = 128

## Used git --git-dir="{absolute_path}/.git" to use git pull origin main without navigating to the project folder.
## Example: git --git-dir="/home/m-shrief/Work/Projects/Adeeb_Astro_SSR/.git" pull origin main

# When using the call command, if the return value is 0, then it's successful.
# call(["git", "clone", "https://github.com/M-Shrief/Adeeb_ExpressTS.git"])