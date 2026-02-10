from __future__ import annotations

from . import handler  # noqa: F401
from .config import Config
from .web import app

from fastapi import FastAPI
from nonebot import get_driver
from nonebot.drivers import ReverseDriver
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-danmaku",
    description="支持命令的弹幕姬",
    usage="访问 /danmaku?room=<房间号> 查看弹幕",
    config=Config,
    homepage="https://github.com/MingxuanGame/live-workspace/tree/master/src/packages/nonebot-plugin-danmaku",
    type="application",
    supported_adapters={"~bilibili_live"},
)
driver = get_driver()

if not isinstance(driver, ReverseDriver) or not isinstance(driver.server_app, FastAPI):
    raise NotImplementedError("Only FastAPI reverse driver is supported.")

driver.server_app.mount("/danmaku", app, name="danmaku")
