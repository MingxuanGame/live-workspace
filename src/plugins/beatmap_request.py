from __future__ import annotations

from typing import Annotated

from src.lib.notification import notifier_manager
from src.lib.osu_api import OsuV1Client

import aiosu
from nonebot import logger, on_command
from nonebot.adapters.bilibili_live import DanmakuEvent, Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata


def is_enabled() -> bool:
    return notifier_manager.current_notifier.startswith("osu_")


__plugin_meta__ = PluginMetadata(
    name="点歌请求",
    description="",
    usage="",
    homepage="https://github.com/MingxuanGame/live-workspace/tree/master/src/plugins/beatmap_request.py",
    type="application",
    supported_adapters={"~bilibili_live"},
    extra={
        "danmaku_commands": [
            {
                "name": "b",
                "description": "点歌",
                "usage": "<beatmap_id> [mods]",
                "enabled": is_enabled,
            }
        ]
    },
)


matcher = on_command(
    "b",
    priority=10,
    block=True,
    rule=is_enabled,
)


class ExitFor(Exception):  # noqa: N818
    pass


@matcher.handle()
async def handle_beatmap_request(
    event: DanmakuEvent,
    args: Annotated[Message, CommandArg()],
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

    notifier_data = {
        "bid": bid_int,
        "mods": mods,
        "beatmapset": beatmapset,
        "beatmap": beatmap,
        "username": event.sender.name,
        "user_id": event.get_user_id(),
    }
    await notifier_manager.emit("beatmap_request", notifier_data)
