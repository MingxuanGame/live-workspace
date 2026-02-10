from __future__ import annotations

from typing import Annotated

from nonebot import get_plugin_config, logger
from nonebot.params import Depends
from pydantic import BaseModel
from simpleobsws import WebSocketClient


class Config(BaseModel):
    obs_address: str = "ws://localhost:4455"
    obs_password: str = ""
    obs_identify_timeout: int = 10


OBS_WEBSOCKET_API: WebSocketClient | None = None

config = get_plugin_config(Config)


async def init_obs():
    global OBS_WEBSOCKET_API
    OBS_WEBSOCKET_API = WebSocketClient(
        url=config.obs_address, password=config.obs_password
    )
    try:
        await OBS_WEBSOCKET_API.connect()
        connedted = await OBS_WEBSOCKET_API.wait_until_identified(
            config.obs_identify_timeout
        )
        if not connedted:
            raise RuntimeError(
                "Timeout while waiting for OBS WebSocket API identification."
            )
    except Exception as e:
        logger.error(f"Failed to connect to OBS WebSocket API: {e}")
        OBS_WEBSOCKET_API = None
        return
    logger.info("OBS WebSocket client connected.")


async def close_obs():
    global OBS_WEBSOCKET_API
    if OBS_WEBSOCKET_API is not None:
        await OBS_WEBSOCKET_API.disconnect()
        OBS_WEBSOCKET_API = None
    logger.success("OBS WebSocket client disconnected.")


def get_obs_websocket_api() -> WebSocketClient:
    """Get OBS WebSocket API client."""
    global OBS_WEBSOCKET_API
    if OBS_WEBSOCKET_API is None:
        raise RuntimeError("OBS WebSocket API client is not initialized.")
    return OBS_WEBSOCKET_API


OBSClient = Annotated[WebSocketClient, Depends(get_obs_websocket_api)]
