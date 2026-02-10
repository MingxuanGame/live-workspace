from __future__ import annotations

from typing import Annotated

from aiohttp import ClientSession
from nonebot.params import Depends

HTTP_CLIENT: ClientSession | None = None


async def init_http_client():
    global HTTP_CLIENT
    if HTTP_CLIENT is None:
        HTTP_CLIENT = ClientSession()


async def close_http_client():
    global HTTP_CLIENT
    if HTTP_CLIENT is not None:
        await HTTP_CLIENT.close()
        HTTP_CLIENT = None


def get_http_client() -> ClientSession:
    """Get HTTP client."""
    global HTTP_CLIENT
    if HTTP_CLIENT is None:
        raise RuntimeError(
            "HTTP client is not initialized. Please call init_http_client first."
        )
    assert HTTP_CLIENT is not None
    return HTTP_CLIENT


HTTPClient = Annotated[ClientSession, Depends(get_http_client)]
