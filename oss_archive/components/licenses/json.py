import json
from pydantic import ValidationError
###
from oss_archive.utils.logger import logger
from oss_archive.config import JSON_LICENSES_PATH
from oss_archive.schemas.license import JSONSchema


def get_licenses_from_json_file()-> list[JSONSchema] | None:
    try:
        if JSON_LICENSES_PATH is None:
            return None
        with open(JSON_LICENSES_PATH, 'r') as file:
            licenses_arr = json.load(file)
            licenses: list[JSONSchema] = []
            for item in licenses_arr:
                new_license = JSONSchema(**item)
                licenses.append(new_license)

            return licenses
    except json.JSONDecodeError as e:
        logger.error(f"Couldn't read {JSON_LICENSES_PATH}", error=e)
        return None
    except ValidationError as e:
        logger.error(f"Error in {JSON_LICENSES_PATH} schema", error=e)
        return None
    except Exception as e:
        logger.error(f"Unknown error in {JSON_LICENSES_PATH}", error=e)
        return None


def write_licenses_file(licenses: list[JSONSchema])->bool:
    try:
        licenses_json = []
        for item in licenses:
            licenses_json.append(item.model_dump())
        
        if JSON_LICENSES_PATH is None:
            return False
        with open(JSON_LICENSES_PATH, "w") as file:
            json.dump(licenses_json, file)
            return True
    except Exception:
        return False