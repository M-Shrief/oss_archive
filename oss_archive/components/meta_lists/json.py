import json
from pydantic import ValidationError
import os
# import mimetypes
from typing import List 
###
from oss_archive.config import JSON_META_LISTS_PATH
from oss_archive.utils.logger import logger
from oss_archive.components.meta_lists.schema import MetaList


def get_meta_lists()->List[MetaList]:
    meta_lists : List[MetaList] = []

    for file in get_meta_lists_files():
        meta_list: MetaList | None = get_meta_list_from_file(file)
        if meta_list is None:
            continue
        meta_lists.append(meta_list)

    return meta_lists


def get_meta_lists_files() -> List[str]:
    meta_lists = [file for file in os.listdir(JSON_META_LISTS_PATH) if file.endswith('.json')]
    return meta_lists

def get_meta_list_from_file(meta_list_file: str)-> MetaList | None:
    try:
        with open(f"{JSON_META_LISTS_PATH}/{meta_list_file}", 'r') as file:
            data = json.load(file)
            return MetaList(**data)
    except json.JSONDecodeError as e:
        logger.error(f"Couldn't read {meta_list_file}", error=e)
        return None
    except ValidationError as e:
        logger.error(f"Error in {meta_list_file} schema", error=e)
        return None
    except Exception as e:
        logger.error(f"Unknown error in {meta_list_file}", error=e)
        return None

def write_meta_list_file(file_name: str, meta_list: MetaList)->bool:
    try:
        with open(f"{JSON_META_LISTS_PATH}/{file_name}", "w") as file:
            json.dump(meta_list.model_dump(), file)
            return True
    except Exception:
        return False

# def get_files_as_dict() -> Dict[str,str]:
#     files_dict = {}
#     for f in os.listdir(OSS_LIST):
#         file_path = os.path.join(OSS_LIST, f)
#         if os.path.isfile(file_path):
#             file_type, _ = mimetypes.guess_type(f)
#             if file_type:
#                 files_dict[f] = file_type
#             else:
#                 files_dict[f] = "Unknown"
#     return files_dict
