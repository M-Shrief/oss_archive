from fastapi import APIRouter, HTTPException, status, Depends
from typing import Any
###
from oss_archive.components.forgejo import requests
from oss_archive.components.forgejo.schema import ForgejoOrganization, ForgejoUser, ForgejoRepo, ForgejoLicense, ForgejoLicensesListItem
from oss_archive.utils.httpx import get_response_metadata
from oss_archive.utils.logger import logger

router = APIRouter(tags=["Forgejo"])


#### Orgs ######################
@router.get(
    path="/forgejo/orgs",
    status_code=status.HTTP_200_OK,
    response_model=list[ForgejoOrganization],
    response_model_exclude_none=True
)
def get_all_orgs() :
    res = requests.get(endpoint="/admin/orgs")
    if res is None:
        return None
    data: list[Any]= res.json()
    if type(data) is not list:
        return None
    orgs: list[ForgejoOrganization] = []
    for item in data:
        org = ForgejoOrganization(**item)
        orgs.append(org)
    return orgs


@router.get(
    path="/forgejo/orgs/{org_name}",
    status_code=status.HTTP_200_OK,
    response_model=ForgejoOrganization,
    response_model_exclude_none=True,
)
def get_org(org_name: str):
    res = requests.get(endpoint=F"/orgs/{org_name}")
    if res is None or res.status_code != 200:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Couldn't find orgs")
    else:
        org = res.json()
        return org


@router.get(
    path="/forgejo/orgs/{org_name}/repos",
    status_code=status.HTTP_200_OK,
    response_model=list[ForgejoRepo],
    response_model_exclude_none=True,
)
def get_orgs_repos(org_name: str):
    try:
        res = requests.get(endpoint=F"/orgs/{org_name}/repos")
        if res is None or res.status_code != 200:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Couldn't get org's repos")
        else:
            data: list[Any] = res.json()
            if type(data) is not list:
                return None
            # return data
            repos: list[ForgejoRepo] = []
            for item in data:
                repo = ForgejoRepo(**item)
                repos.append(repo)
            return repos
    except Exception as e:
        logger.error('error', error=e)
        return 


##############################
