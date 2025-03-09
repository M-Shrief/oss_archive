from pydantic import BaseModel
### 
from oss_archive.utils import schemas

class OSSoftware(
    schemas.IdField,
    schemas.OSSoftwareNameField,
    schemas.OSSoftwareDescriptionField,
    schemas.OSSoftwareTopicsField,
    schemas.ReviewedField,
    schemas.OSSoftwareLatestVersionField,
    schemas.OSSoftwareHTMLURLField,
    schemas.OSSoftwareAPIURLField,
    schemas.OSSoftwareCloneURLField,

    # schemas.OSSListKeyRelatedField,
    # schemas.OwnerIdRelatedField,
    # schemas.LicenseKeyRelatedField,

    schemas.CreatedAtField,
    schemas.UpdatedAtField,
    BaseModel
    ):
    ### Relations
    oss_list: schemas.PopulatedOSSList 
    owner: schemas.PopulatedOwner
    license: schemas.PopulatedLicense
