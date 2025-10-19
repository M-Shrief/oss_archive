
from pydantic import Field, BaseModel
from datetime import datetime
from typing import Annotated
from uuid import UUID
from enum import Enum

### General Fields

class ActionsEnum(str, Enum):
    ArchiveOnly = "archive_only"
    ArchiveAll = "archive_all"
    ArchiveAllExcept = "archive_all_except"


class OwnerTypeEnum(str, Enum):
    Individual = "Individual"
    Organization = "Organization"

class DevelopmentStatusEnum(str, Enum):
    Ongoing = "Ongoing"
    Stalled = "Stalled"
    Stopped = "Stopped"

class IdField(BaseModel):
    id: UUID

class PriorityField(BaseModel):
    priority: Annotated[int, Field(ge=1, le=10)]

class PriorityField_Optional(BaseModel):
    priority: Annotated[int | None, Field(default=None, ge=1, le=10)]


class ReviewedField(BaseModel):
    reviewed:  Annotated[bool, Field(default=False)]

class ReviewedField_Optional(BaseModel):
    reviewed:  Annotated[bool | None, Field(default=None)]

class CreatedAtField(BaseModel):
    created_at: datetime

class UpdatedAtField(BaseModel):
    updated_at: datetime


# General relations' fields
class MainCategoryKeyField(BaseModel):
    main_category_key: Annotated[str, Field(max_length=256, examples=["ai"])]

class MainCategoryKeyField_Optional(BaseModel):
    main_category_key: Annotated[str | None, Field(default=None, max_length=256, examples=["ai"])]

class OwnerUsernameField(BaseModel):
    owner_username: Annotated[str, Field(max_length=256, examples=["deepseek-ai"])]
class OwnerUsernameField_Optional(BaseModel):
    owner_username: Annotated[str | None, Field(default=None, max_length=256, examples=["deepseek-ai"])]
