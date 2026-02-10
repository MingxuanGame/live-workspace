from __future__ import annotations

from nonebot import get_plugin_config
from pydantic import BaseModel, Field


class Config(BaseModel):
    debug: bool = Field(alias="danmaku_debug", default=False)


config = get_plugin_config(Config)
