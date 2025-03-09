from pydantic import BaseModel
###
from oss_archive.utils import schemas

class License(
    schemas.LicenseKeyField,
    schemas.LicenseNameField,
    schemas.LicenseHTMLURLField,
    schemas.LicenseAPIURLField,
    BaseModel
    ):
    pass
