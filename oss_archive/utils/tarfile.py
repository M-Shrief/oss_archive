import os
import tarfile
### 
from oss_archive.utils import paths
from oss_archive.utils.logger import logger

async def compress(oss_fullname: str) -> bool:
    """compress OSS directory"""
    try:
        archive_path = paths.get_oss_archive_path(oss_fullname)
        compressed_archive_path = paths.get_oss_compressed_archive_path(oss_fullname)
        with tarfile.open(compressed_archive_path, 'w:gz') as tar_file:
            tar_file.add(archive_path, arcname=os.path.basename(archive_path))
        
        return True
    except Exception as e:
        logger.error("Error compressing the directory", error=e) 
        return False
    

async def decompress(oss_fullname: str) -> bool:
    """decompress OSS's tarfile"""
    try:
        archive_path = paths.get_oss_archive_path(oss_fullname)
        compressed_archive_path = paths.get_oss_compressed_archive_path(oss_fullname)

        with tarfile.open(compressed_archive_path, "r") as tar:
            tar.extractall(archive_path)
        return True
    except Exception as e:
        logger.error("Error decompressing tar file" , error=e) 
        return False