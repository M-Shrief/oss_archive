import os
import tarfile
### 
from oss_archive.config import ARCHIVE_BASE_PATH
from oss_archive.utils.logger import logger

async def compress(dir_name: str) -> bool:
    try:
        path = f"{ARCHIVE_BASE_PATH}/{dir_name}"
        with tarfile.open(f"{path}.tar", 'w:gz') as tar_file:
            tar_file.add(path, arcname=os.path.basename(path))
        
        return True
    except Exception as e:
        logger.error("Error compressing the directory", error=e) # pyright:ignore[reportCallIssue]
        return False
    

async def decompress(file_name: str) -> bool:
    try:
        path = f"{ARCHIVE_BASE_PATH}/{file_name}"
        if ARCHIVE_BASE_PATH is None:
            raise Exception("Archive path is not defined")

        with tarfile.open(path, "r") as tar:
            tar.extractall(path=ARCHIVE_BASE_PATH)
        return True
    except Exception as e:
        logger.error("Error decompressing tar file" , error=e) # pyright:ignore[reportCallIssue]
        return False