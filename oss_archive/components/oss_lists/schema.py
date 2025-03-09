from pydantic import BaseModel
from typing import List
##
from oss_archive.utils import schemas 

class OSSList(
    schemas.OSSListKeyField,
    schemas.OSSListNameField,
    schemas.OSSListTagsField,
    schemas.PriorityField,
    schemas.ReviewedField,
    schemas.CreatedAtField,
    schemas.UpdatedAtField,
    BaseModel
    ):
    ### Relations
    owners: List[schemas.PopulatedOwner]
    os_softwares: List[schemas.PopulatedOSSoftware]

