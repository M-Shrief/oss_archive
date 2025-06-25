
from pydantic import Field, BaseModel
from datetime import datetime
from typing import Annotated
from uuid import UUID
from enum import Enum

### General Fields

class ActionsType(str, Enum):
    ArchiveAll = "archive_all"
    ArchiveOnly = "archive_only"
    ArchiveExcept = "archive_except"


class OwnerType(str, Enum):
    Individual = "Individual"
    Organization = "Organization"

class IdField(BaseModel):
    id: UUID

class PriorityField(BaseModel):
    priority: Annotated[int, Field(ge=1, le=10)]

class ReviewedField(BaseModel):
    reviewed:  Annotated[bool, Field(default=False)]

class CreatedAtField(BaseModel):
    created_at: datetime

class UpdatedAtField(BaseModel):
    updated_at: datetime


# General relations' fields
class MetaListKeyField(BaseModel):
    meta_list_key: Annotated[str, Field(max_length=256, examples=["ai"])]

class MetaItemIdField(BaseModel):
    meta_item_id: UUID

class LicenseKeyField(BaseModel):
    license_key: Annotated[str, Field(max_length=256, examples=["MIT"])]
