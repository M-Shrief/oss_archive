from pydantic import Field, BaseModel
from typing import Annotated
### 


class KeyField(BaseModel):
    key: Annotated[str, Field(max_length=128, examples=["mit"])]

class NameField(BaseModel):
    name: Annotated[str, Field(max_length=128, examples=["MIT"])]

class FullnameField(BaseModel):
    fullname: Annotated[str, Field(max_length=128, examples=["MIT License"])]

class HTMLURLField(BaseModel):
    html_url: Annotated[str, Field(max_length=128, examples=["http://choosealicense.com/licenses/mit/"])]

class APIURLField(BaseModel):
    api_url: Annotated[str, Field(max_length=128, examples=["https://api.github.com/licenses/mit"])]


class FullSchema(
    KeyField,
    NameField,
    FullnameField,
    HTMLURLField,
    APIURLField,
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
    FullnameField,
    HTMLURLField,
    APIURLField,
    ):
    pass