from httpx import Headers
### 
from oss_archive.config import Forgejo

base_headers = Headers(
    headers={
        "Authorization": f"token {Forgejo.get("access_token")}",
        "Content-Type": "application/json",
        }
    )