from pydantic import Field, BaseModel
from typing import Annotated
from datetime import datetime
### 
from oss_archive.schemas.general import IdField, ReviewedField, MetaListKeyField, MetaItemIdField, LicenseKeyField, CreatedAtField, UpdatedAtField

class NameField(BaseModel):
    name: Annotated[str, Field(max_length=256, examples=["DeepSeek-VL"])]

class FullnameField(BaseModel):
    fullname: Annotated[str, Field(max_length=256, examples=["deepseek-ai:DeepSeek-VL"])]

class DescriptionField(BaseModel):
    description: Annotated[str | None, Field(examples=["DeepSeek-VL: Towards Real-World Vision-Language Understanding"])]

class TopicsField(BaseModel):
    topics: Annotated[list[str] | None, Field(examples=[["foundation-models","vision-language-model","vision-language-pretraining"]])]

class IsArchived(BaseModel):
    is_archived: Annotated[bool, Field(default=False)]

class DateOfArchiveField(BaseModel):
    date_of_archive: Annotated[datetime | None, Field(default=None)]

class CreatedAtSourceField(BaseModel):
    created_at_source: Annotated[datetime | None, Field(default=None)]

class UpdatedAtSourceField(BaseModel):
    updated_at_source:  Annotated[datetime | None, Field(default=None)]

class HTMLURLField(BaseModel):
    html_url: Annotated[str, Field(examples=["https://github.com/deepseek-ai/DeepSeek-VL"])]

class CloneURLField(BaseModel):
    clone_url: Annotated[str, Field(examples=["https://github.com/deepseek-ai/DeepSeek-VL.git"])]

class FullSchema(
    IdField,
    NameField,
    FullnameField,
    DescriptionField,
    TopicsField,
    ReviewedField,
    IsArchived,
    DateOfArchiveField,
    CreatedAtSourceField,
    UpdatedAtSourceField,
    HTMLURLField,
    CloneURLField,
    CreatedAtField,
    UpdatedAtField,

    MetaListKeyField,
    MetaItemIdField,
    LicenseKeyField,
    ):
    pass

class DescriptiveSchema(
    IdField,
    NameField,
    DescriptionField,
    IsArchived,
    DateOfArchiveField,
    HTMLURLField,
    CloneURLField,

    MetaListKeyField,
    MetaItemIdField,
    LicenseKeyField,
    ):
    pass

class MinimalSchema(
    IdField,
    NameField,
    ):
    pass