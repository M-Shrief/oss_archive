from pydantic import BaseModel, Field 
from typing import Annotated
### 
from oss_archive.schemas import general
from oss_archive.schemas import oss

class KeyField(BaseModel):
    key: Annotated[str, Field(max_length=256, examples=["ai"])]

class KeyField_Optional(BaseModel):
    key: Annotated[str | None, Field(default=None, max_length=256, examples=["ai"])]

class NameField(BaseModel):
    name: Annotated[str, Field(max_length=256, examples=["Artifical Inteligience (AI)"])]

class NameField_Optional(BaseModel):
    name: Annotated[str | None, Field(default=None, max_length=256, examples=["Artifical Inteligience (AI)"])]

class DescriptionField(BaseModel):
    description: Annotated[str, Field(examples=["Artifical Inteligience and it's applications, like LLMs and others."])]

class DescriptionField_Optional(BaseModel):
    description: Annotated[str | None, Field(default=None, examples=["Artifical Inteligience and it's applications, like LLMs and others."])]

class TopicsField(BaseModel):
    topics: Annotated[list[str], Field(examples=[["AI", "Machine Learning"]])]    

class TopicsField_Optional(BaseModel):
    topics: Annotated[list[str] | None, Field(default=None, examples=[["AI", "Machine Learning"]])]    



class FullSchema(
    KeyField,
    NameField,
    DescriptionField,
    TopicsField,
    general.PriorityField, 
    general.ReviewedField, 
    general.CreatedAtField,
    general.UpdatedAtField
    ):
    pass

class DescriptiveSchema(
    KeyField,
    NameField,
    DescriptionField,
    TopicsField,
    general.PriorityField, 
    general.ReviewedField, 
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
    DescriptionField,
    TopicsField,
    general.PriorityField, 
    general.ReviewedField, 
    ):
    # main_oss: Annotated[list[oss.JSONSchema], Field(default=[])]
    # related_oss: Annotated[list[os_software.JSONSchema], Field(default=[])]
    pass