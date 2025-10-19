from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime

from sqlalchemy.orm.base import PASSIVE_CLASS_MISMATCH
### 
from oss_archive.schemas import general

class UsernameField(BaseModel):
    username: Annotated[str, Field(max_length=256, examples=["deepseek-ai"])]

class UsernameField_Optional(BaseModel):
    username: Annotated[str | None, Field(default=None, max_length=256, examples=["deepseek-ai"])]

class NameField(BaseModel):
    name: Annotated[str | None, Field(default=None, max_length=256, examples=["DeepSeek"])]

class NameField_Optional(NameField):
    pass 

class TypeField(BaseModel):
    type: Annotated[general.OwnerTypeEnum, Field(examples=[general.OwnerTypeEnum.Organization])]

class TypeField_Optional(BaseModel):
    type: Annotated[general.OwnerTypeEnum | None, Field(default=None, examples=[general.OwnerTypeEnum.Organization])]

class SourceField(BaseModel):
    source: Annotated[str, Field(max_length=256, examples=["github"])]

class SourceField_Optional(BaseModel):
    source: Annotated[str | None, Field(default=None, max_length=256, examples=["github"])]

class OtherSourcesField(BaseModel):
    other_sources: Annotated[list[str], Field(max_length=256, default=[], description="A list of HTML urls for the source, which is used to upate meta item data if needed")]

class OtherSourcesField_Optional(BaseModel):
    other_sources: Annotated[list[str] | None, Field(default=None, max_length=256, description="A list of HTML urls for the source, which is used to upate meta item data if needed")]

class ActionsField(BaseModel):
    actions: Annotated[general.ActionsEnum, Field(examples=[general.ActionsEnum.ArchiveAll])]

class ActionsField_Optional(BaseModel):
    actions: Annotated[general.ActionsEnum | None, Field(default=None, examples=[general.ActionsEnum.ArchiveAll])]

class ActionsOnField(BaseModel):
    actions_on: Annotated[list[str], Field(default=[], description="A list of repo names which we'll use to apply actions on them, and we only extract the name of the repo without the owner's name.")]

class ActionsOnField_Optional(BaseModel):
    actions_on: Annotated[list[str] | None, Field(default=None, description="A list of repo names which we'll use to apply actions on them, and we only extract the name of the repo without the owner's name.")]

class HTMLURLField(BaseModel):
    html_url: Annotated[str | None, Field(max_length=256, default=None)]

class HTMLURLField_Optional(HTMLURLField):
    pass

# Add main_category_key field
class FullSchema(
    general.IdField,
    UsernameField,
    NameField,
    TypeField,
    SourceField,
    OtherSourcesField,
    ActionsField,
    ActionsOnField,
    HTMLURLField,
    general.PriorityField,
    general.ReviewedField,
    general.CreatedAtField,
    general.UpdatedAtField,
    # Relations
    general.MainCategoryKeyField,
    ):
    pass
 
class DescriptiveSchema(
    general.IdField,
    UsernameField,
    NameField,
    TypeField,
    SourceField,
    OtherSourcesField,
    ActionsField,
    ActionsOnField,
    HTMLURLField,
    general.PriorityField,
    general.ReviewedField,
    # Relations
    general.MainCategoryKeyField,
    ):
    pass

class MinimalSchema(
    general.IdField,
    UsernameField,
    NameField,
    TypeField,
    general.PriorityField,
    ):
    pass

class JSONSchema(
    UsernameField,
    NameField,
    TypeField,
    SourceField,
    OtherSourcesField,
    ActionsField,
    ActionsOnField,
    HTMLURLField,
    general.PriorityField,
    general.ReviewedField,
    # Relations
    general.MainCategoryKeyField,
    ):
    pass
