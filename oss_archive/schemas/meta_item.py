from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime
### 
from oss_archive.schemas.general import OwnerType, ActionsType, IdField, PriorityField, ReviewedField, CreatedAtField, UpdatedAtField


class HTMLURLField(BaseModel):
    html_url: Annotated[str | None, Field(max_length=256, default=None)]

class OwnerUsernameField(BaseModel):
    owner_username: Annotated[str, Field(max_length=256, examples=["ai"])]

class OwnerNameField(BaseModel):
    owner_name: Annotated[str, Field(max_length=256, examples=["ai"])]
    
class OwnerTypeField(BaseModel):
    owner_type: Annotated[OwnerType, Field()]

class OwnerCreatedAtField(BaseModel):
    owner_created_at: Annotated[datetime | None, Field(default=None)]

class OwnerUpdatedAtField(BaseModel):
    owner_updated_at:  Annotated[datetime | None, Field(default=None)]

class SourceField(BaseModel):
    source: Annotated[str, Field(max_length=256, examples=["github"])]

class OtherSourcesField(BaseModel):
    other_sources: Annotated[list[str], Field(max_length=256, default=[], examples=[["github", "gitlab"]])]

class ActionsField(BaseModel):
    actions: Annotated[ActionsType, Field(default=ActionsType.DownloadAll)]

class ActionsOnField(BaseModel):
    actions_on: Annotated[list[str], Field(default=[])]


class FullSchema(
    IdField,
    HTMLURLField,
    PriorityField,
    ReviewedField,
    
    OwnerUsernameField,
    OwnerNameField,
    OwnerTypeField,
    OwnerCreatedAtField,
    OwnerUpdatedAtField,

    SourceField,
    OtherSourcesField,

    ActionsField,
    ActionsOnField,
    
    CreatedAtField,
    UpdatedAtField
    ):
    pass
 
class DescriptiveSchema(
    IdField,
    HTMLURLField,

    OwnerUsernameField,
    OwnerNameField,
    OwnerTypeField,

    SourceField,


    PriorityField,
    ReviewedField,
    ):
    pass

class MinimalSchema(
    IdField,
    OwnerUsernameField,
    SourceField,
    ):
    pass

class JSONSchema(
    HTMLURLField,

    OwnerUsernameField,
    OwnerTypeField,

    SourceField,
    OtherSourcesField,

    ActionsField,
    ActionsOnField,

    PriorityField,
    ReviewedField,
    ):
    pass
