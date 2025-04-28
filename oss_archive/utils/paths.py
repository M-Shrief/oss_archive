from datetime import datetime
import os 
###
from oss_archive.utils.logger import logger
from oss_archive.config import ARCHIVE_BASE_PATH, COMPRESSED_ARCHIVE_BASE_PATH

def get_oss_archive_path(oss_fullname: str) -> str:
    return f"{ARCHIVE_BASE_PATH}/{oss_fullname}"

def get_oss_compressed_archive_path(oss_fullname: str) -> str:
    return f"{COMPRESSED_ARCHIVE_BASE_PATH}/{oss_fullname}.tar"


def does_path_exists(path: str) -> bool | None:
    try:
        return os.path.exists(path)
    except OSError as e:
        logger.error("Couldn't check if content exists or not", error=e)
        return None
    except Exception as e:
        logger.error("Unknown error checking if content exists or not", error=e)
        return None

def get_path_info(path: str):
    try:
        info = os.stat(path)
        return {
            'creation_time': datetime.fromtimestamp(info.st_ctime).date(),
            'modification_time':  datetime.fromtimestamp(info.st_mtime).date(),
            # 'access_time':  datetime.fromtimestamp(info.st_atime).date(),
            'size': f"{info.st_size} Bytes",
            # 'permissions': info.st_mode,
            # 'owner': info.st_uid,
            # 'group': info.st_gid
        }
    except OSError as e:
        logger.error("Couldn't get content info", error=e)
        return
    except Exception as e:
        logger.error("Unknown error, Couldn't get content info", error=e)
        return