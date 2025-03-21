import os
import tarfile
### 
from oss_archive.config import ARCHIVE_BASE_PATH

async def compress(dir_name: str):
    path = f"{ARCHIVE_BASE_PATH}/{dir_name}"
    with tarfile.open(f"{path}.tar", 'w:gz') as tar_file:
        tar_file.add(path, arcname=os.path.basename(path))
    
    return
    

async def decompress(file_name: str):
    path = f"{ARCHIVE_BASE_PATH}/{file_name}"
    try:
        with tarfile.open(path, "r") as tar:
            tar.extractall(path=ARCHIVE_BASE_PATH)
        print("Tar file decompressed successfully.")
    except Exception as e:
        print(f"Error decompressing tar file: {e}")