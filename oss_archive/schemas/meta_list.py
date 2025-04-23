from pydantic import BaseModel, Field 
from typing import Annotated
### 
from oss_archive.schemas.general import PriorityField, ReviewedField, CreatedAtField, UpdatedAtField
from oss_archive.schemas import meta_item

class KeyField(BaseModel):
    key: Annotated[str, Field(max_length=256, examples=["ai"])]

class NameField(BaseModel):
    name: Annotated[str, Field(max_length=256, examples=["ai"])]


class TagsField(BaseModel):
    tags: Annotated[list[str], Field(examples=[["AI", "Machine Learning"]])]    


class FullSchema(
    KeyField,
    NameField,
    TagsField,
    PriorityField, 
    ReviewedField, 
    CreatedAtField,
    UpdatedAtField
    ):
    pass

class DescriptiveSchema(
    KeyField,
    NameField,
    TagsField,
    PriorityField, 
    ReviewedField, 
    ):
    pass


class MinimalSchema(
    KeyField,
    NameField,
    ):
    pass

class JSONSchema(
    KeyField,
    NameField,
    TagsField,
    PriorityField, 
    ReviewedField, 
    ):
    ### actual data
    items: Annotated[list[meta_item.JSONSchema], Field(default=[])]
