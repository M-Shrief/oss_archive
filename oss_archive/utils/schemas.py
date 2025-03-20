from pydantic import Field, BaseModel
from datetime import datetime
from typing import Annotated, List
from uuid import UUID
from enum import Enum

### General Fields
class IdField(BaseModel):
    id: UUID

class PriorityField(BaseModel):
    priority: Annotated[int, Field(ge=1, le=10)]

class ReviewedField(BaseModel):
    reviewed:  Annotated[bool, Field(default=False)]

class IsSeededField(BaseModel):
    is_seeded: Annotated[bool, Field(default=False)]
class CreatedAtField(BaseModel):
    created_at: datetime

class UpdatedAtField(BaseModel):
    updated_at: datetime

### OSSList's Fields
class OSSListKeyField(BaseModel):
    key: Annotated[str, Field(examples=["ai"])]

class OSSListNameField(BaseModel):
    name: Annotated[str, Field(examples=["AI, Machine Learning, LLMs,...etc"])]

class OSSListTagsField(BaseModel):
    tags: Annotated[List[str], Field(examples=[["AI","Machine Learning","LLMs"]])]

### Owner's Fields

class OwnerType(str, Enum):
    Individual = "Individual"
    Organization = "Organization"

class OwnerNameField(BaseModel):
    name: Annotated[str, Field(examples=["DeepSeek"])]

class OwnerUsernameField(BaseModel):
    username: Annotated[str, Field(examples=["deepseek-ai"])]

class OwnerSourceField(BaseModel):
    source: Annotated[str, Field(examples=["github", "custom"])]

class OwnerTypeField(BaseModel):
    type: Annotated[OwnerType, Field(examples=["Individual", "Organization"])]

class OwnerHTMLURLField(BaseModel):
    html_url: Annotated[str, Field(examples=["https://github.com/orgs/deepseek-ai"])]

class OwnerAPIURLField(BaseModel):
    api_url: Annotated[str, Field(examples=["https://api.github.com/orgs/deepseek-ai"])]

### License's Fields
class LicenseKeyField(BaseModel):
    key: Annotated[str, Field(max_length=128, examples=["mit"])]

class LicenseNameField(BaseModel):
    name: Annotated[str, Field(max_length=128, examples=["MIT"])]

class LicenseFullnameField(BaseModel):
    fullname: Annotated[str, Field(max_length=128, examples=["MIT License"])]

class LicenseHTMLURLField(BaseModel):
    html_url: Annotated[str, Field(max_length=128, examples=["http://choosealicense.com/licenses/mit/"])]

class LicenseAPIURLField(BaseModel):
    api_url: Annotated[str, Field(max_length=128, examples=["https://api.github.com/licenses/mit"])]

### OSSoftware's Fields

class OSSoftwareNameField(BaseModel):
    name: Annotated[str, Field(max_length=256, examples=["DeepSeek-VL"])]

class OSSoftwareDescriptionField(BaseModel):
    description: Annotated[str | None, Field(examples=["DeepSeek-VL: Towards Real-World Vision-Language Understanding"])]

class OSSoftwareTopicsField(BaseModel):
    topics: Annotated[List[str] | None, Field(examples=[["foundation-models","vision-language-model","vision-language-pretraining"]])]

class OSSoftwareLatestVersionField(BaseModel):
    latest_version: bool

class OSSoftwareHTMLURLField(BaseModel):
    html_url: Annotated[str, Field(examples=["https://github.com/deepseek-ai/DeepSeek-VL"])]

class OSSoftwareAPIURLField(BaseModel):
    api_url: Annotated[str, Field(examples=["https://api.github.com/repos/deepseek-ai/DeepSeek-VL"])]

class OSSoftwareCloneURLField(BaseModel):
    clone_url: Annotated[str, Field(examples=["https://github.com/deepseek-ai/DeepSeek-VL.git"])]

### Relations' specific Fields
class OSSListKeyRelatedField(BaseModel):
    oss_list_key: Annotated[str, Field(examples=["ai"])]

class OwnerIdRelatedField(BaseModel):
    owner_id: UUID

class LicenseKeyRelatedField(BaseModel):
    license_key: Annotated[str, Field(examples=["mit"])]



### Populated Relations' Fields
class PopulatedOSSList(
    OSSListKeyField,
    OSSListNameField,
    BaseModel
    ):
    pass

class PopulatedOwner(
    IdField,
    OwnerUsernameField,
    OwnerNameField,
    BaseModel
    ):
    pass

class PopulatedOSSoftware(
    IdField,
    OSSoftwareNameField,
    BaseModel
    ):
    pass

class PopulatedLicense(
    LicenseKeyField,
    LicenseNameField,
    BaseModel
    ):
    pass
