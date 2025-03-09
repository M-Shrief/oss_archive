import json
from pydantic import ValidationError
from typing import List 
###
from oss_archive.utils.logger import logger
from oss_archive.config import JSON_LICENSES_PATH
from oss_archive.components.licenses.schema import License

def get_licenses_from_json_file()-> List[License] | None:
    try:
        with open(JSON_LICENSES_PATH, 'r') as file:
            licenses_arr = json.load(file)
            licenses: List[License] = []
            for item in licenses_arr:
                new_license = License(**item)
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
