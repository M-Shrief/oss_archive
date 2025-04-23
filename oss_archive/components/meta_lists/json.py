import json
from pydantic import ValidationError
import os
###
from oss_archive.config import JSON_META_LISTS_PATH
from oss_archive.utils.logger import logger
from oss_archive.schemas.meta_list import JSONSchema 


def get_meta_lists()->list[JSONSchema]:
    meta_lists : list[JSONSchema] = []

    for file in get_meta_lists_files():
        meta_list: JSONSchema | None = get_meta_list_from_file(file)
        if meta_list is None:
            continue
        meta_lists.append(meta_list)

    return meta_lists


def get_meta_lists_files() -> list[str]:
    meta_lists = [file for file in os.listdir(JSON_META_LISTS_PATH) if file.endswith('.json')]
    return meta_lists

def get_meta_list_from_file(meta_list_file: str)-> JSONSchema | None:
    """meta_list_file naming convention is {key}.json"""
    try:
        with open(f"{JSON_META_LISTS_PATH}/{meta_list_file}", 'r') as file:
            data = json.load(file)
            return JSONSchema(**data)
    except json.JSONDecodeError as e:
        logger.error(f"Couldn't read {meta_list_file}", error=e)
        return None
    except ValidationError as e:
        logger.error(f"Error in {meta_list_file} schema", error=e)
        return None
    except Exception as e:
        logger.error(f"Unknown error in {meta_list_file}", error=e)
        return None

def write_meta_list_file(meta_list: JSONSchema)->bool:
    try:
        with open(f"{JSON_META_LISTS_PATH}/{meta_list.key}.json", "w") as file:
            json.dump(meta_list.model_dump(), file)
            return True
    except Exception:
        return False
