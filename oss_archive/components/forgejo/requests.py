from httpx import RequestError, NetworkError, HTTPStatusError, ConnectError, ReadError, Timeout
from httpx import URL, Client, Cookies, Headers, Response, QueryParams
from typing import Any
###
from oss_archive.config import Forgejo
from oss_archive.utils.httpx import ASYNC_TRANSPORT, SYNC_TRANSPORT, DEFAULT_TIMEOUT
from oss_archive.utils.logger import logger



base_headers = Headers(
    headers={
        "Authorization": f"token {Forgejo.get("access_token")}",
        "Content-Type": "application/json",
        }
    )

def get(endpoint: str, params: QueryParams | None=None, timeout: Timeout = DEFAULT_TIMEOUT)-> Response | None:
    """A helper function to make a GET request to Forgejo API,
    adding the required headers for authentication,
    and adding the endpoint parameter to the API url.
    
    example for endpoint paramater: /admin/orgs"""
    try:
        with Client(transport=SYNC_TRANSPORT, timeout=timeout) as client:
            response = client.get(
                url=f"{Forgejo.get("base_url")}{endpoint}",
                params=params,
                headers=base_headers,
            )

            return response
    except NetworkError:
        logger.error("network error while making the request")
        return None
    except HTTPStatusError as e:
        return e.response
    except RequestError as e:
        logger.error("Error while making a request", error=e)
        return None

def post(endpoint: str, body: Any, timeout: Timeout = DEFAULT_TIMEOUT)-> Response | None:
    """A helper function to make a GET request to Forgejo API,
    adding the required headers for authentication,
    and adding the endpoint parameter to the API url.
    
    example for endpoint paramater: /admin/orgs"""
    try:
        with Client(transport=SYNC_TRANSPORT, timeout=timeout) as client:
            response = client.post(
                url=f"{Forgejo.get("base_url")}{endpoint}",
                headers=base_headers,
                json=body
            )

            return response
    except NetworkError:
        logger.error("network error while making the request")
        return None
    except HTTPStatusError as e:
        return e.response
    except RequestError as e:
        logger.error("Error while making a request", error=e)
        return None


def patch(endpoint: str, body: Any, timeout: Timeout = DEFAULT_TIMEOUT)-> Response | None:
    """A helper function to make a GET request to Forgejo API,
    adding the required headers for authentication,
    and adding the endpoint parameter to the API url.
    
    example for endpoint paramater: /admin/orgs"""
    try:
        with Client(transport=SYNC_TRANSPORT, timeout=timeout) as client:
            response = client.patch(
                url=f"{Forgejo.get("base_url")}{endpoint}",
                headers=base_headers,
                json=body
            )

            return response
    except NetworkError:
        logger.error("network error while making the request")
        return None
    except HTTPStatusError as e:
        return e.response
    except RequestError as e:
        logger.error("Error while making a request", error=e)
        return None
    
def delete(endpoint: str, timeout: Timeout = DEFAULT_TIMEOUT)-> Response | None:
    """A helper function to make a GET request to Forgejo API,
    adding the required headers for authentication,
    and adding the endpoint parameter to the API url.
    
    example for endpoint paramater: /admin/orgs"""
    try:
        with Client(transport=SYNC_TRANSPORT, timeout=timeout) as client:
            response = client.delete(
                url=f"{Forgejo.get("base_url")}{endpoint}",
                headers=base_headers,
            )

            return response
    except NetworkError:
        logger.error("network error while making the request")
        return None
    except HTTPStatusError as e:
        return e.response
    except RequestError as e:
        logger.error("Error while making a request", error=e)
        return None