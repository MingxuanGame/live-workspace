from __future__ import annotations

from typing import Annotated

import aiosu
from nonebot import get_plugin_config
from nonebot.params import Depends
from pydantic import BaseModel


class Config(BaseModel):
    osu_api_v1_apikey: str


config = get_plugin_config(Config)


async def osu_v1_client():
    async with aiosu.v1.Client(config.osu_api_v1_apikey) as client:
        yield client


OsuV1Client = Annotated[aiosu.v1.Client, Depends(osu_v1_client)]
