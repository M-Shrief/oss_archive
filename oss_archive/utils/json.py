import json
from pydantic import BaseModel, ValidationError, Field
from typing import Annotated, TypedDict, Any
import os
###
from oss_archive.config import JSON_FILES_PATH
from oss_archive.utils.logger import logger
from oss_archive.utils.formatter import format_file_name
# from oss_archive.schemas.category import JSONSchema as CategoryJSONSchema
# from oss_archive.schemas.owner import JSONSchema as OwnerJSONSchema
# from oss_archive.schemas.oss import JSONSchema as OSSJSONSchema


def sync_json():
    """
    1 - First define what you're syncing: Categories, Owners or OSS
    2 - Get the data and sorted by priority first, then sort every priority group alphabetically. 
    3 - Delete old files in the path related to the data, so that we have the recent files only.
    4 - Start syncing and writing the data in it's related by path,
        we write the data to files by having every file's items which doesn't exceed max_length the was defined.
        Every file have a name that is defined by a convention "{categories|owners|oss}-file_number}"
        and that file_number related to first items group, second group,...etc.          
    """
    pass

DEFAULT_MAX_LENGTH = 100 # used as a max_length for the list of blocks in blocks' JSON file.

class JSONFile(
    BaseModel,
    ):
    priority: Annotated[int, Field(ge=1, le=10)]
    file_number: Annotated[int, Field(default=1, ge=1)]
    items: Annotated[list[Any], Field(default=[], max_length=DEFAULT_MAX_LENGTH)]



class JSONFileConfigType(TypedDict):
    name_prefix: str
    json_dir: str
    items_max_length: int

CategoriesJSONFileConfig = JSONFileConfigType(name_prefix="categories", json_dir=f"{JSON_FILES_PATH}categories/", items_max_length=DEFAULT_MAX_LENGTH)
OwnersJSONFileConfig = JSONFileConfigType(name_prefix="owners", json_dir=f"{JSON_FILES_PATH}owners/", items_max_length=DEFAULT_MAX_LENGTH)
OSSJSONFileConfig = JSONFileConfigType(name_prefix="oss", json_dir=f"{JSON_FILES_PATH}oss/", items_max_length=DEFAULT_MAX_LENGTH)



def del_files(config: JSONFileConfigType):
    """Delete all JSON files"""
    files = [file for file in os.listdir(config.get("json_dir")) if file.endswith('.json')]
    for file in files:   
        os.remove(path=config.get("json_dir")+file)

    return None

def write_json_files(config: JSONFileConfigType, items: list[Any]):
    """Every file will have a max number of items = DEFAULT_MAX_LENGTH, the naming convention will use a standard function: get_block_file_name()"""
    # Seperate blocks by their priority, using it's priority as a key for the dict.
    priority_items: dict[int, list[Any]] = {}
    for item in items: 
            if priority_items.get(item.priority) is None:
                priority_items[item.priority] = []

            priority_items[item.priority].append(item)

    for key,value in priority_items.items():
        __write_files(config, priority=key, items=value)

    return

def __write_files(config: JSONFileConfigType, priority: int, items: list[Any]):
    items_count = len(items)
    # Here we get the count of files we need, like if len(blocks) = 2500, it'll be:
    # (2440 + (100-2440%100)) / 100 = 25.0 --> converted to int by int(25.0) = 25
    files_count = int((items_count + (DEFAULT_MAX_LENGTH - items_count % DEFAULT_MAX_LENGTH)) / DEFAULT_MAX_LENGTH)

    # list's start & end are used to slice the array, like [start:end]...etc
    list_start = 0
    list_end = DEFAULT_MAX_LENGTH
    file_number = 1

    while file_number <= files_count:

        json_file = JSONFile(
            priority=priority,
            file_number=file_number,
            items=items[list_start:list_end]
            )

        _ = __write_file(config, json_file, file_number )
        list_start += DEFAULT_MAX_LENGTH
        list_end += DEFAULT_MAX_LENGTH
        file_number += 1


def __write_file(config: JSONFileConfigType, json_file: JSONFile, file_number: int)->bool:
    file_name = format_file_name(config.get("name_prefix"), json_file.priority, file_number)
    try:
        with open(config.get("json_dir") + f"{file_name}.json", "w") as file:
            json.dump(json_file.model_dump(mode='json'), file)
            return True
    except Exception as e:
        logger.error("Couldn't write JSON file", file_name=file_name, error=e)
        return False

