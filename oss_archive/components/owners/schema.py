from pydantic import BaseModel
from typing import List


###
from oss_archive.utils import schemas

class Owner(
    schemas.IdField,
    # schemas.OSSListKeyRelatedField,
    schemas.OwnerNameField,
    schemas.OwnerUsernameField,
    schemas.OwnerSourceField,
    schemas.OwnerTypeField,
    schemas.ReviewedField,
    schemas.OwnerHTMLURLField,
    schemas.OwnerAPIURLField,
    schemas.CreatedAtField,
    schemas.UpdatedAtField,
    BaseModel
    ):
    ### Relations
    oss_list: schemas.PopulatedOSSList
    os_softwares: List[schemas.PopulatedOSSoftware]