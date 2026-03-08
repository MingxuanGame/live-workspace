from __future__ import annotations

from typing import Any

from src.lib.notification import register_notifier

from aiohttp import ClientSession
from aiosu.models import Beatmap, Beatmapset
from nonebot import get_plugin_config, logger
from pydantic import BaseModel


class Config(BaseModel):
    notifier_osu_lazer_server: str = "http://localhost:34790"


config = get_plugin_config(Config)

notifier = register_notifier("osu_lazer")


@notifier.handle("beatmap_request")
async def handle_beatmap_request(
    data: dict[str, Any],
) -> None:
    mods: str = data["mods"]
    bid_int: int = data["bid"]
    beatmapset: Beatmapset = data["beatmapset"]
    beatmap: Beatmap = data["beatmap"]
    username: str = data["username"]

    display_mod_str = f"+{mods}" if mods else ""
    async with ClientSession() as session:
        await session.post(
            f"{config.notifier_osu_lazer_server}/notification",
            json={
                "icon": "Solid.Music",
                "message": (
                    f"{username} 点歌: "
                    f"{beatmapset.artist} - {beatmapset.title} [{beatmap.version}] "
                    f"{display_mod_str}"
                ),
                "operation": {
                    "type": "OpenLink",
                    "data": {"url": f"https://osu.ppy.sh/b/{bid_int}"},
                },
            },
        )
        logger.info(
            f"Sent beatmap request notification for bid {bid_int} with mods {mods}."
            f" (username: {username})"
        )


@notifier.handle("message")
async def handle_message(
    data: dict[str, Any],
) -> None:
    event = data["event"]
    message = event.get_message()
    sender_name = event.sender.name
    async with ClientSession() as session:
        await session.post(
            f"{config.notifier_osu_lazer_server}/notification",
            json={
                "icon": "Regular.CommentAlt",
                "message": f"{sender_name}: {message}",
            },
        )
        logger.info(f"Sent message notification: {sender_name}: {message}")
