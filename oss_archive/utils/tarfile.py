import os
import tarfile
### 
from oss_archive.config import ARCHIVE_BASE_PATH, COMPRESSED_ARCHIVE_BASE_PATH
from oss_archive.utils.logger import logger

async def compress(oss_fullname: str) -> bool:
    """compress OSS directory"""
    try:
        if ARCHIVE_BASE_PATH is None or COMPRESSED_ARCHIVE_BASE_PATH is None:
            raise Exception("Compressed Archive's path is not defined")
            
        archive_path = f"{ARCHIVE_BASE_PATH}/{oss_fullname}"
        compressed_archive_path = f"{COMPRESSED_ARCHIVE_BASE_PATH}/{oss_fullname}.tar"
        with tarfile.open(compressed_archive_path, 'w:gz') as tar_file:
            tar_file.add(archive_path, arcname=os.path.basename(archive_path))
        
        return True
    except Exception as e:
        logger.error("Error compressing the directory", error=e) 
        return False
    

async def decompress(oss_fullname: str) -> bool:
    """decompress OSS's tarfile"""
    try:
        if ARCHIVE_BASE_PATH is None or COMPRESSED_ARCHIVE_BASE_PATH is None:
            raise Exception("Compressed Archive's path is not defined")

        archive_path = f"{ARCHIVE_BASE_PATH}/{oss_fullname}"
        compressed_archive_path = f"{COMPRESSED_ARCHIVE_BASE_PATH}/{oss_fullname}.tar"

        with tarfile.open(compressed_archive_path, "r") as tar:
            tar.extractall(archive_path)
        return True
    except Exception as e:
        logger.error("Error decompressing tar file" , error=e) 
        return False