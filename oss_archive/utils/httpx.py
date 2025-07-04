"""httpx config module to standardize our requests, adding retries, error handling and other features."""
from typing import TypedDict, Any
from datetime import timedelta
from httpx import URL, Client, Cookies, Headers, Response, QueryParams, AsyncClient, Timeout
from httpx import AsyncHTTPTransport, HTTPTransport
from httpx import RequestError, NetworkError, HTTPStatusError, ConnectError, ReadError
###
from oss_archive.utils.logger import logger

### Retries
# We can use tenacity(https://tenacity.readthedocs.io/en/latest/) to configure more complex logic
SYNC_TRANSPORT = HTTPTransport(retries=3)
ASYNC_TRANSPORT = AsyncHTTPTransport(retries=3)

DEFAULT_TIMEOUT = Timeout(5.0, connect=5.0)

DEFAULT_HEADERS = Headers(headers={"Content-Type": "application/json"})


class ResponseMetadata(TypedDict):
    url: URL
    headers: Headers
    cookies: Cookies
    time_elapsed: timedelta

def get_response_metadata(res: Response) -> ResponseMetadata:
    url = res.url
    headers = res.headers
    cookies = res.cookies
    time_elapsed = res.elapsed

    return ResponseMetadata(url=url, headers=headers, cookies=cookies, time_elapsed=time_elapsed)

def get(base_url: str, endpoint: str, timeout: Timeout = DEFAULT_TIMEOUT, headers: Headers = DEFAULT_HEADERS)-> Response | None:
    """A helper function to make a sync GET request using httpx,
    and adding the endpoint parameter to the base url.
    
    example for endpoint paramater: /admin/orgs"""
    try:
        with Client(transport=SYNC_TRANSPORT, timeout=timeout) as client:
            response = client.get(
                url=base_url + endpoint,
                headers=headers,
            )

            return response
    except NetworkError as e:
        logger.error("network error while making the request", error=e)
        return None
    except HTTPStatusError as e:
        return e.response
    except RequestError as e:
        logger.error("Error while making a request", error=e)
        return None

async def async_get(base_url: str, endpoint: str, timeout: Timeout = DEFAULT_TIMEOUT, headers: Headers = DEFAULT_HEADERS)-> Response | None:
    """A helper function to make an async GET request using httpx,
    and adding the endpoint parameter to the base url.
    
    example for endpoint paramater: /admin/orgs"""
    try:
        async with AsyncClient(transport=ASYNC_TRANSPORT, timeout=timeout) as client:
            response = await client.get(
                url=base_url + endpoint,
                headers=headers,
            )
            return response
    except NetworkError as e:
        logger.error("network error while making the request", error=e)
        return None
    except HTTPStatusError as e:
        return e.response
    except RequestError as e:
        logger.error("Error while making a request", error=e)
        return None

