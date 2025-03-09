from pydantic import BaseModel, Field
from typing import Annotated, List
from enum import Enum
###
from oss_archive.utils.schemas import PriorityField, OwnerType

### For json_meta_lists files
class DownloadActions(str, Enum):
    All = "all"
    Only = "only"
    Except = "except"

class Repo(BaseModel):
    name: Annotated[str, Field(max_length=256, examples=["fastapi"])]
    html_url: Annotated[str | None, Field(max_length=256,examples=["https://github.com/fastapi/fastapi"], default=None)]
    api_url: Annotated[str | None, Field(max_length=256,examples=["https://api.github.com/repos/fastapi/fastapi"], default=None)]
    clone_url: Annotated[str, Field(max_length=256, examples=["https://github.com/fastapi/fastapi.git"])]

class Actions(BaseModel):
    download: Annotated[DownloadActions, Field()]
    selected_repos: Annotated[List[str], Field(examples=[["repo_name_1", "repo_name_2"]])]
    repos_details: Annotated[List[Repo], Field(examples=[], default=[])]

class MetaItem(PriorityField, BaseModel):
    owner: Annotated[str, Field(max_length=256, examples=["ai"])]
    type: Annotated[OwnerType, Field()]
    source: Annotated[str, Field(max_length=256, examples=["github"])]

    html_url: Annotated[str | None, Field(max_length=256, default=None)]
    reviewed: Annotated[bool, Field(default=False)]
    actions: Annotated[Actions | None, Field(default=None)]

class MetaList(PriorityField, BaseModel):
    key: Annotated[str, Field(max_length=256, examples=["ai"])]
    name: Annotated[str, Field(max_length=256, examples=["ai"])]
    tags: Annotated[List[str], Field(examples=[["AI", "Machine Learning"]])]
    reviewed: Annotated[bool, Field(default=False)]

    ### actual data
    items: Annotated[List[MetaItem], Field(examples=[{"name": "deepseek-ai","type": "Organization","source": "github","priority": 1}])]
