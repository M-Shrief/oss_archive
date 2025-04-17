from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, validates
from sqlalchemy import DateTime, Enum, ARRAY, String, text, SmallInteger, Integer, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID
from typing import List
###
from oss_archive.utils.schemas import OwnerType
from oss_archive.components.meta_lists.schema import ActionsType

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass

class PriorityField():
    """Adding a priority field for the model
    the priority is an integer range from 1 to 10, the smaller the more important it is."""
    priority: Mapped[int] = mapped_column(SmallInteger())
    @validates("priority")
    def validate_priority(self, key, priority):
        if priority < 1 or priority > 10:
            raise ValueError("Priority should be between 1 and 10")
        return priority

class MetaList(PriorityField, Base):
    __tablename__ = "meta_lists"

    key: Mapped[str] = mapped_column(String(length=128), primary_key=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(length=256), nullable=True)
    tags: Mapped[List[str]] = mapped_column(ARRAY(String(length=128)), default=[])
    reviewed: Mapped[bool] = mapped_column(Boolean(), default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(DateTime(), server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))

    # Relations
    meta_items: Mapped[List["MetaItem"]] = relationship(back_populates="meta_list")
    os_softwares: Mapped[List["OSSoftware"]] = relationship(back_populates="meta_list")


class MetaItem(PriorityField, Base):
    __tablename__ = "meta_items"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True, nullable=False)
    reviewed: Mapped[bool] = mapped_column(Boolean(), default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(DateTime(), server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))

    # Owner's data from external sources
    owner_username: Mapped[str] = mapped_column(String(length=256), unique=True, nullable=False)
    owner_name: Mapped[str | None] = mapped_column(String(length=256), nullable=True, default=None)
    owner_type: Mapped[OwnerType] = mapped_column(Enum(OwnerType, name="owner_type", native_enum=True), nullable=False)
    ### The Date the owner signed up for the other platform (github, gitlab...etc)
    owner_created_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
    ### the last time the owner's data was updated
    owner_updated_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)

    # URLs
    html_url: Mapped[str | None] = mapped_column(String(length=256), nullable=True)

    # Sources
    source: Mapped[str] = mapped_column(String(length=128), nullable=False)
    other_sources: Mapped[List[str]] = mapped_column(ARRAY(String(length=128)), default=[])

    # Actions
    actions: Mapped[ActionsType] = mapped_column(Enum(ActionsType, name="actions_type", native_enum=True), nullable=False)
    actions_on: Mapped[List[str]] = mapped_column(ARRAY(String(128)), default=[])

    ### data about the repos
    seeded_repos: Mapped[bool] = mapped_column(Boolean(), default=False)
    repos_count: Mapped[int] = mapped_column(Integer(), default=0)
    newest_repo_date: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)


    ### Relations
    meta_list_key: Mapped[str] = mapped_column(ForeignKey("meta_lists.key"), nullable=False)
    meta_list: Mapped["MetaList"] = relationship(back_populates="meta_items")
    os_softwares: Mapped[List["OSSoftware"]] = relationship(back_populates="meta_item")


# We don't use "OSS" abbreviation so that we can differentiate between singular and plural names, even though it's cooler.
class OSSoftware(Base):
    __tablename__ = "os_softwares"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(DateTime(), server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))


    name: Mapped[str] = mapped_column(String(length=256), nullable=False)
    fullname: Mapped[str] = mapped_column(String(length=256), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(length=256), nullable=True)
    topics: Mapped[List[str]] = mapped_column(ARRAY(String(128)), default=[]) # we gets the field data from the API
    reviewed: Mapped[bool] = mapped_column(Boolean(), default=False)
    latest_version: Mapped[bool] = mapped_column(Boolean(), default=False)  # did we archive the latest version of the oss?
    ### The Date the oss's repo was created in th source
    oss_created_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=False)
    ### the last time the oss's repo was updated in th source
    oss_updated_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=False)

    # URLs
    ### oss page (html page)
    html_url: Mapped[str | None] = mapped_column(String(length=256), nullable=True)
    ### oss's api endpoint
    api_url: Mapped[str | None] = mapped_column(String(length=256), nullable=True)
    ### git clone's URL
    clone_url: Mapped[str | None] = mapped_column(String(length=256), nullable=True)

    ### Relations
    meta_list_key: Mapped[str] = mapped_column(ForeignKey("meta_lists.key"), nullable=False)
    meta_list: Mapped["MetaList"] = relationship(back_populates="os_softwares")

    meta_item_id: Mapped[str] = mapped_column(ForeignKey("meta_items.id"), nullable=False)
    meta_item: Mapped["MetaItem"] = relationship(back_populates="os_softwares")

    license_key: Mapped[str] = mapped_column(ForeignKey("licenses.key"), default="unknown")
    license: Mapped["License"] = relationship()



# Get the data from: https://api.github.com/licenses
# And see each license name,html_url,description,license_body,
class License(Base):
    __tablename__ = "licenses"

    # No need for id field because they're a handful of items, we use the key field as the primary key.

    # A key for the licenses, like MIT licenses -> mit, and on.
    key: Mapped[str] = mapped_column(String(length=128), primary_key=True, nullable=False)
    fullname: Mapped[str | None] = mapped_column(String(length=128), nullable=True)
    name: Mapped[str | None] = mapped_column(String(length=128), nullable=True)

    # URLs
    ### License's page
    html_url: Mapped[str | None] = mapped_column(String(length=256), nullable=True)
    ### License's API
    api_url: Mapped[str | None] = mapped_column(String(length=256), nullable=True)
