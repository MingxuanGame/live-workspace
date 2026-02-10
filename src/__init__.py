from __future__ import annotations

from src.lib.http import close_http_client, init_http_client
from src.lib.obs import close_obs, init_obs
from src.lib.tosu import start_tosu_websocket, stop_tosu_websocket

from nonebot import get_driver

driver = get_driver()


@driver.on_startup
async def _():
    await init_http_client()
    await init_obs()
    await start_tosu_websocket()


@driver.on_shutdown
async def _():
    await stop_tosu_websocket()
    await close_obs()
    await close_http_client()
