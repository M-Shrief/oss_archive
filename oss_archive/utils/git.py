from subprocess import run, call, CompletedProcess
###
from oss_archive.config import ARCHIVE_BASE_PATH
from oss_archive.utils.logger import logger


async def clone(clone_url: str, owner_username: str, repo_name: str) -> tuple[CompletedProcess[bytes], bool]:
    # returns zero, if it's successful.
    # call(["git", "clone", "https://github.com/M-Shrief/Adeeb_ExpressTS.git"])
    result: CompletedProcess[bytes] = run(args=["git", "clone", clone_url, f"{ARCHIVE_BASE_PATH}/{owner_username}:{repo_name}"], capture_output=True)
    if result.returncode != 0:
        logger.error(f"Error when cloning {clone_url}", git_result=result) 
        return result, False
        
    return result, True


async def push():
    pass

# class ReturnCodes(Enum):
#     Success = 0
#     Err_Unfinished = 128


## Use git --git-dir="{absolute_path}/.git" to use git pull origin main without navigating to the project folder.
## Example: git --git-dir="/home/m-shrief/Work/Projects/Adeeb_Astro_SSR/.git" pull origin main
async def pull():
    pass