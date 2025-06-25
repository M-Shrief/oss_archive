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

#### Users ######################
@router.get(
    path="/forgejo/users",
    status_code=status.HTTP_200_OK,
    response_model=list[ForgejoUser],
    response_model_exclude_none=True
)
def get_all_users() :
    res = requests.get(endpoint="/admin/users")
    if res is None or res.status_code != 200:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Couldn't get users")
    data: list[Any]= res.json()
    if type(data) is not list:
        return None

    users: list[ForgejoUser] = []
    for item in data:
        user = ForgejoUser(**item)
        users.append(user)
    return users


@router.get(
    path="/forgejo/users/{username}",
    status_code=status.HTTP_200_OK,
    response_model=ForgejoUser,
    response_model_exclude_none=True,
)
def get_user(username: str):
    res = requests.get(endpoint=F"/users/{username}")
    if res is None or res.status_code != 200:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Couldn't find user")
    else:
        user= res.json()
        return user


@router.get(
    path="/forgejo/users/{username}/repos",
    status_code=status.HTTP_200_OK,
    response_model=list[ForgejoRepo],
    response_model_exclude_none=True
)
def get_user_repos(username: str):
    res = requests.get(endpoint=F"/users/{username}/repos")
    if res is None or res.status_code != 200:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Couldn't find user")
    data: list[Any] = res.json()
    if type(data) is not list:
        return None

    repos: list[ForgejoRepo] = []
    for item in data:
        repo = ForgejoRepo(**item)
        repos.append(repo)
    return repos


@router.post(
    path="/forgejo/users",
    status_code=status.HTTP_201_CREATED,
    response_model=ForgejoUser,
    response_model_exclude_none=True,
)
def add_user(user_data: dict[str, Any]):
    #   "email": "example2@mail.com",
    #   "username": "example2",
    #   "login_name": "example2",
    #   "password": "P@ssword1"
    try:
        result = requests.post(endpoint="/admin/users", body=user_data)
        if result is None:
            raise Exception("Couldn't create user")
        new_user: ForgejoUser = result.json()
        return new_user
    except Exception as e:
        logger.error("Couldn't add new user", error=e)
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="Error: Couldn't add the new user, try again!")


@router.delete(
    path="/forgejo/users/{username}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model_exclude_none=True
)
def delete_user(username: str):
        result = requests.delete(endpoint=f"/admin/users/{username}")
        if result is not None and result.status_code == 204:
            return
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Couldn't find user")

# def add_org_to_user():
#     # POST "/admin/users/{username}/orgs"
#     pass


# def edit_user():
#     # Patch "/admin/users/{username}"
#     pass


# def add_repo_to_user():
#     # POST "/admin/users/{username}/repos"
#     pass
##############################

