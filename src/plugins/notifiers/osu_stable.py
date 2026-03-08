from __future__ import annotations

import asyncio
from typing import Annotated, Any

from src.lib.notification import register_notifier

from aiosu.models import Beatmap, Beatmapset
from nonebot import get_driver, get_plugin_config, logger
from nonebot.params import Depends
from pydantic import BaseModel
import pydle

IRC_ADDRESS = "irc.ppy.sh"


class Config(BaseModel):
    notifier_osu_stable_username: str
    notifier_osu_stable_password: str
    notifier_osu_stable_target: str


config = get_plugin_config(Config)

notifier = register_notifier("osu_stable")


class IrcBot(pydle.features.RFC1459Support):
    async def on_connect(self):
        logger.success("Connected to IRC server.")

    async def _create_user(self, nickname):
        # Servers are NOT users.
        if not nickname or "." in nickname:
            return

        self.users[nickname] = {
            "nickname": nickname,
            "username": None,
            "realname": None,
            "hostname": None,
        }


client = IrcBot(
    config.notifier_osu_stable_username,
    username=config.notifier_osu_stable_username,
)
IrcClient = Annotated[IrcBot, Depends(lambda: client)]
task = None

driver = get_driver()


@driver.on_startup
async def startup():
    global task
    task = asyncio.create_task(
        client.connect(
            IRC_ADDRESS,
            password=config.notifier_osu_stable_password,
        )
    )
    logger.info("Connecting to IRC server...")


@driver.on_shutdown
async def shutdown():
    await client.disconnect()
    if task is not None:
        task.cancel()


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
    await client.message(
        config.notifier_osu_stable_target,
        (
            f"{username} 点歌: "
            f"[https://osu.ppy.sh/b/{bid_int} {beatmapset.artist} - {beatmapset.title} star{beatmap.difficulty_rating:.2f} [{beatmap.version}]] "  # noqa: E501
            f"{display_mod_str} (bid: {bid_int})"
        ),
    )
    logger.info(
        f"Sent beatmap request notification for bid {bid_int} with mods {mods}."
        f" (username: {username})"
    )
