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


@router.post(
    path="/forgejo/orgs",
    status_code=status.HTTP_201_CREATED,
    response_model=ForgejoOrganization,
    response_model_exclude_none=True,
)
def create_org_for_user(data: dict[str, Any]):
    try:
        username = data["username"]
        
        request_body = {"username": data["org_name"]}
        result  = requests.post(endpoint=f"/admin/users/{username}/orgs", body=request_body)
        if result is None:
            raise Exception("Couldn't create org")
        # if result.status_code != 201:
        #     raise error
        #     pass

        new_org: ForgejoUser = result.json()
        return new_org
    except Exception as e:
        logger.error("Couldn't add new org", error=e)
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="Error: Couldn't add the new org, try again!")


# @router.post(
#     path="/forgejo/orgs/repos",
#     status_code=status.HTTP_201_CREATED,
#     response_model=ForgejoRepo,
#     response_model_exclude_none=True,
# )
# def create_repo_for_org(data: dict[str, Any]):
#     try:
#         org_name = data["org_name"]
#         req_body = {}
#         result  = requests.post(endpoint=f"/admin/users/{org_name}/repos", body=req_body)
#         if result is None:
#             raise Exception("Couldn't create repo for org")
        # if result.status_code != 201:
        #     raise error
        #     pass
#         new_org: ForgejoUser = result.json()
#         return new_org
#     except Exception as e:
#         logger.error("Couldn't create repo for org", error=e)
#         raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="Error: Couldn't create repo for org, try again!")

@router.delete(
    path="/forgejo/orgs/{org_name}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model_exclude_none=True
)
def delete_org(org_name: str):
    result = requests.delete(endpoint=f"/orgs/{org_name}")
    if result is not None and result.status_code == 204:
        return
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Couldn't find user")


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
        # if result.status_code != 201:
        #     # raise error
        #     pass

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


#### Repos ################

@router.get(
    "/forgejo/repos",
    status_code=status.HTTP_200_OK,
    response_model=list[ForgejoRepo],
    response_model_exclude_none=True
)
async def get_repos(page: int = 1, limit: int = 10):
    res = requests.get(endpoint=f"/repos/search?page={page}&limit={limit}")
    if res is None or res.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error while getting repos")
    result = res.json()
    repos = result["data"]
    return repos


@router.get(
    "/forgejo/repos/{owner}/{repo}",
    status_code=status.HTTP_200_OK,
    response_model=ForgejoRepo,
    response_model_exclude_none=True
)
async def get_repo(owner: str, repo: str):
    res = requests.get(endpoint=f"/repos/{owner}/{repo}")
    if res is None or res.status_code != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repo is not Found")
    repo = res.json()
    return repo


@router.post(
"/forgejo/repos/migrate",
    status_code=status.HTTP_201_CREATED,
    response_model=ForgejoRepo,
    response_model_exclude_none=True
)
async def migrate_repo(body: dict[str, Any]):
    # {
        # "clone_addr": str
        # "repo_name": str
        # "repo_owner": str
        # "service": Enum[ git, github, gitea, gitlab, gogs, onedev, gitbucket, codebase ]
        # "mirror": bool
        # "mirror_interval": str
    # }
    try:
        result = requests.post(endpoint="/repos/migrate", body=body)
        if result is None:
            logger.error("Migrating error", result=result)
            raise Exception("Couldn't migrate repo")
        # if result.status_code != 201:
        #     raise error
        #     pass
        new_repo: ForgejoUser = result.json()
        return new_repo
    except Exception as e:
        logger.error("Couldn't add migrate repo", error=e)
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="Error: Couldn't add the new user, try again!")


    
##############################


#### Licenses ################
@router.get(
    "/forgejo/licenses",
    status_code=status.HTTP_200_OK,
    response_model=list[ForgejoLicensesListItem],
    response_model_exclude_none=True
)
async def get_licenses():
    res = requests.get(endpoint="/licenses")
    if res is None or res.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error while getting licenses")
    licenses = res.json()
    return licenses

@router.get(
    "/forgejo/licenses/{key}",
    status_code=status.HTTP_200_OK,
    response_model=ForgejoLicense,
    response_model_exclude_none=True
)
async def get_license_by_key(key: str):
    res = requests.get(endpoint=f"/licenses/{key}")
    if res is None or res.status_code != 200:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Couldn't find license")
    
    license: ForgejoLicense = res.json()
    return license

##############################

