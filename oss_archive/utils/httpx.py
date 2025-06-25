"""httpx config module to standardize our requests, adding retries, error handling and other features."""
from typing import TypedDict
from datetime import timedelta


from httpx import URL, Client, Cookies, Headers, Response, Timeout
from httpx import AsyncHTTPTransport, HTTPTransport
# HTTPX's errors
# from httpx import RequestError, NetworkError, HTTPStatusError, ConnectError, ReadError
# Get Request params
# from httpx import URL, Client, Cookies, Headers, Response
###
# from oss_archive.utils.logger import logger


### Suggestion
# We can make a factory class to initiate every time and get the an instance we want.

### Retries
# We can use tenacity(https://tenacity.readthedocs.io/en/latest/) to configure more complex logic
SYNC_TRANSPORT = HTTPTransport(retries=3)
ASYNC_TRANSPORT = AsyncHTTPTransport(retries=3)

DEFAULT_TIMEOUT = Timeout(20.0, connect=10.0)


# client = Client(
#     transport=SYNC_TRANSPORT,
#     timeout=DEFAULT_TIMEOUT
#     )

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

# def sync_get(url: URL | str, *, params: QueryParamTypes | None=None, headers: HeaderTypes | None=None, cookies: CookieTypes | None=None, auth: AuthTypes | UseClientDefault | None=USE_CLIENT_DEFAULT, follow_redirects: bool | UseClientDefault=USE_CLIENT_DEFAULT, timeout: TimeoutTypes | UseClientDefault=USE_CLIENT_DEFAULT, extensions: RequestExtensions | None=None)->Response | None:
#     try:
#         with Client(transport=SYNC_TRANSPORT) as client:
#             response = client.get(
#                 url=url,
#                 params=params,
#                 headers=headers,
#                 cookies=cookies,
#                 auth=auth,
#                 follow_redirects=follow_redirects,
#                 timeout=timeout,
#                 extensions=extensions
#             )

#             return response
#     except NetworkError:
#         logger.error("network error while making the request")
#         return None
#     except HTTPStatusError as e:
#         return e.response
#     except RequestError as e:
#         logger.error("Error while making a request", error=e)
#         return None
