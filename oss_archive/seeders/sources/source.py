from typing import List, Dict, Any, Protocol
from sqlalchemy.ext.asyncio import AsyncSession
###
from oss_archive.database.models import Owner, OSSoftware
from oss_archive.components.meta_lists.schema import MetaItem



class Source(Protocol):
    """A Protocol to make a stable interface for every source that we should adhere to
    
    Note: It's not used now, but in the future we'll need this or something like it, so that we standardize our work"""
    API_BASE_URL: str        # This is a protocol member
    
    async def add_meta_item(meta_item: MetaItem, db: AsyncSession) -> (Owner | None, List[OSSoftware] | None):     # This is a protocol member
        raise NotImplementedError

    async def add_owner_from_meta_item(meta_item: MetaItem, db: AsyncSession) -> Owner | None:
        raise NotImplementedError

    async def add_owner_repos(owner: Owner, db: AsyncSession) -> List[OSSoftware] | None:
        raise NotImplementedError

    async def get_individual(meta_list_key: str, meta_item: MetaItem)-> Owner | None:
        """Get the Individual's data from {source} API and return it as an Owner Model"""
        raise NotImplementedError

    async def get_org(meta_list_key: str, meta_item: MetaItem)->Owner | None:
        """Get the Organization's data from {source} API and return it as an Owner Model"""
        raise NotImplementedError

    def __get_new_owner(meta_list_key: str, meta_item: MetaItem, api_response: dict[str, Any]) -> Owner | None:
        """Get the needed data from {source} API into the Owner Model"""
        raise NotImplementedError

    def __get_new_oss(meta_list_key: str, owner: Owner, repo_dict: Dict[str, Any]) -> OSSoftware | None:
        """Get the needed data from {source} API response - from the owner's repo array - to create a OSS model."""
        raise NotImplementedError

    def get_html_url(owner_username: str)->str:
        # return f"source_html_url_convention/{owner_username}"
        raise NotImplementedError

    def get_api_url(owner_username: str)->str:
        # return f"source_api_url_convention/{owner_username}"
        raise NotImplementedError

    def get_clone_url(owner_username: str, repo_name: str)->str:
        # return f"source_clone_url_convention/{meta_item.owner}"
        raise NotImplementedError
    