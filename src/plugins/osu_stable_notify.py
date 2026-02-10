from __future__ import annotations

import asyncio
from typing import Annotated

from src.lib.osu_api import OsuV1Client

import aiosu
from nonebot import get_driver, get_plugin_config, logger, on_command
from nonebot.adapters.bilibili_live import DanmakuEvent, Message
from nonebot.params import CommandArg, Depends
from nonebot.plugin import PluginMetadata
from pydantic import BaseModel
import pydle

IRC_ADDRESS = "irc.ppy.sh"


class Config(BaseModel):
    notify_osu_stable_username: str
    notify_osu_stable_password: str
    notify_osu_stable_target: str


config = get_plugin_config(Config)

__plugin_meta__ = PluginMetadata(
    name="notify provider - osu! stable",
    description="",
    usage="",
    config=Config,
    homepage="https://github.com/MingxuanGame/live-workspace/tree/master/src/plugins/osu_stable_notify.py",
    type="application",
    supported_adapters={"~bilibili_live"},
    extra={
        "danmaku_commands": [
            {
                "name": "b",
                "description": "点歌",
                "usage": "<beatmap_id> [mods]",
            }
        ]
    },
)


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
    config.notify_osu_stable_username,
    username=config.notify_osu_stable_username,
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
            password=config.notify_osu_stable_password,
        )
    )
    logger.info("Connecting to IRC server...")


@driver.on_shutdown
async def shutdown():
    await client.disconnect()
    if task is not None:
        task.cancel()


matcher = on_command("b")


class ExitFor(Exception):  # noqa: N818
    pass


@matcher.handle()
async def handle_beatmap_request(
    event: DanmakuEvent,
    args: Annotated[Message, CommandArg()],
    irc: IrcClient,
    osu_client: OsuV1Client,
):
    logger.info(f"Received beatmap request: {args}")
    texts = args.extract_plain_text().strip().split()

    bid = str(texts[0])
    if not bid.isdigit():
        await matcher.finish()
    bid_int = int(bid)

    mods = str(texts[1]) if len(texts) > 1 else ""

    beatmapsets = []
    try:
        for mode in range(4):
            beatmapsets = await osu_client.get_beatmap(
                beatmap_id=bid_int, mode=mode, mods=mods
            )
            if not beatmapsets or len(beatmapsets) == 0:
                continue
            else:
                raise ExitFor()
        logger.info(f"Beatmap request: {bid} not found in any mode.")
        await matcher.finish()
    except aiosu.exceptions.APIException as e:
        logger.error(f"Beatmap request: {bid} APIException occurred: {e}")
        await matcher.finish()
    except ExitFor:
        pass
    beatmapset = beatmapsets[0]
    if beatmapset.beatmaps is None or len(beatmapset.beatmaps) == 0:
        logger.info(f"No beatmaps found for Beatmapset with Beatmap ID {bid_int}.")
        await matcher.finish()
    beatmap = beatmapset.beatmaps[0]
    display_mod_str = f"+{mods}" if mods else ""
    await irc.message(
        config.notify_osu_stable_target,
        (
            f"{event.sender.name} 点歌: "
            f"[https://osu.ppy.sh/b/{bid_int} {beatmapset.artist} - {beatmapset.title} star{beatmap.difficulty_rating:.2f} [{beatmap.version}]] "  # noqa: E501
            f"{display_mod_str} (bid: {bid_int})"
        ),
    )
