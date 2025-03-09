from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, validates
from sqlalchemy import Column, DateTime, Enum, ARRAY, String, text, SmallInteger, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID
from typing import List
###
from oss_archive.utils.schemas import OwnerType

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass

class PriorityField():
    """Adding a priority field for the model
    the priority is an integer range from 1 to 10, the smaller the more important it is."""
    priority: Mapped[int] = Column(SmallInteger())
    @validates("priority")
    def validate_priority(self, key, priority):
        if priority < 1 or priority > 10:
            raise ValueError("Priority should be between 1 and 10")
        return priority

class OSSList(PriorityField, Base):
    __tablename__ = "oss_lists"

    key: Mapped[str] = Column(String(length=128), primary_key=True, nullable=False)
    name: Mapped[str] = Column(String(length=256), nullable=True)
    tags: Mapped[List[str]] = Column(ARRAY(String(length=128)), nullable=True)
    reviewed: Mapped[bool] = Column(Boolean(), default=True)

    owners: Mapped[List["Owner"]] = relationship(back_populates="oss_list")
    os_softwares: Mapped[List["OSSoftware"]] = relationship(back_populates="oss_list")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column( # Check if onupdate works or not.
        DateTime(), server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP")
    )

class Owner(PriorityField, Base):
    __tablename__ = "owners"

    id: Mapped[UUID] = Column(PG_UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True, nullable=False)

    # relations 
    oss_list_key: Mapped[str] = Column(ForeignKey("oss_lists.key"), nullable=False)
    oss_list: Mapped["OSSList"] = relationship(back_populates="owners")
    os_softwares: Mapped[List["OSSoftware"]] = relationship(back_populates="owner")


    # names used for signup and login, but it doesn't adhere to formal names' rules
    username: Mapped[str] = Column(String(length=256), unique=True, nullable=False)
    # Real/Actual/Organizational Names
    name: Mapped[str | None] = Column(String(length=256), nullable=True)

    source: Mapped[str] = Column(String(length=128), nullable=False)
    # Owner's type
    type: Mapped[OwnerType] = Column(Enum(OwnerType, name="owner_type", native_enum=True), nullable=False)
    # Owner's page
    html_url: Mapped[str] = Column(String(length=256), nullable=True)
    # Owner's api endpoint
    api_url: Mapped[str] = Column(String(length=256), nullable=True)

    reviewed: Mapped[bool] = Column(Boolean(), default=False)

    ### The Date the owner signed up for the other platform (github, gitlab...etc)
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    ### the last time the owner's data was updated
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)


# We don't use "OSS" abbreviation so that we can differentiate between singular and plural names, even though it's cooler.
class OSSoftware(Base):
    __tablename__ = "os_softwares"

    id: Mapped[UUID] = Column(PG_UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True, nullable=False)

    name: Mapped[str] = Column(String(length=256), nullable=False)
    fullname: Mapped[str] = Column(String(length=256), unique=True, nullable=False)
    description: Mapped[str] = Column(String(length=256), nullable=True)
    topics: Mapped[List[str]] = Column(ARRAY(String(128)), nullable=True) # we gets the field data from the API
    reviewed: Mapped[bool] = Column(Boolean(), default=False)

    latest_version: Mapped[bool] = Column(Boolean(), default=False)  # did we archive the latest version of the oss?

    ### Relations
    oss_list_key: Mapped[str] = Column(ForeignKey("oss_lists.key"), nullable=False)
    oss_list: Mapped["OSSList"] = relationship(back_populates="os_softwares")

    owner_id: Mapped[UUID] = Column(ForeignKey("owners.id"), nullable=False)
    owner: Mapped["Owner"] = relationship(back_populates="os_softwares")

    license_key: Mapped[str] = Column(ForeignKey("licenses.key"), default="unknown")
    license: Mapped["License"] = relationship()

    ### oss page (html page)
    html_url: Mapped[str] = Column(String(length=256), nullable=True)
    ### oss's api endpoint
    api_url: Mapped[str] = Column(String(length=256), nullable=True)
    ### git clone's URL
    clone_url: Mapped[str] = Column(String(length=256), nullable=True)

    ### The Date the oss's repo was created
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    ### the last time the oss's repo was updated
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

# Get the data from: https://api.github.com/licenses
# And see each license name,html_url,description,license_body,
class License(Base):
    __tablename__ = "licenses"

    # No need for id field because they're a handful of items, we use the key field as the primary key.

    # A key for the licenses, like MIT licenses -> mit, and on.
    key: Mapped[str] = Column(String(length=128), primary_key=True, nullable=False)
    fullname: Mapped[str] = Column(String(length=128), nullable=True)
    name: Mapped[str] = Column(String(length=128), nullable=True)

    # License's page
    html_url: Mapped[str] = Column(String(length=256), nullable=True)
    # License's API
    api_url: Mapped[str] = Column(String(length=256), nullable=True)
