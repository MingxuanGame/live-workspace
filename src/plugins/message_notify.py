from __future__ import annotations

from src.lib.notification import BliveNotifier

from nonebot import on_message
from nonebot.adapters.bilibili_live import DanmakuEvent

matcher = on_message(priority=1000)


@matcher.handle()
async def handle_message(
    event: DanmakuEvent,
    notifier: BliveNotifier,
):
    notifier_data = {
        "event": event,
    }
    await notifier.emit("message", notifier_data)
