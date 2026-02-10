from __future__ import annotations

import time
from typing import cast

from .models import (
    DanmakuData,
    EnterLeaveData,
    ExtendedEmoticon,
    GiftData,
    GuardData,
    LikeData,
    SuperChatData,
    WSMessage,
)
from .web import WSManager

from nonebot import on
from nonebot.adapters.bilibili_live import (
    DanmakuEvent,
    GuardBuyEvent,
    LikeEvent,
    Message,
    SendGiftEvent,
    SuperChatEvent,
    UserEnterEvent,
)

matcher = on()

AVATAR_CACHE: dict[str, str] = {}


def proxy(url: str) -> str:
    """生成代理URL"""
    return f"/danmaku/proxy/{url}"


def message_to_str(message: Message) -> str:
    """将 Message 对象转换为字符串"""
    s = []
    for seg in message:
        if seg.type == "text":
            s.append(str(seg))
        elif seg.type == "emoticon":
            s.append(seg.data["emoji"])
    return "".join(s)


@matcher.handle()
async def handle_danmaku(event: DanmakuEvent, manager: WSManager):
    AVATAR_CACHE[event.get_user_id()] = proxy(event.sender.face)
    emots = cast(
        list[ExtendedEmoticon], list(event.emots.values()) if event.emots else []
    )
    for emot in emots:
        emot["url"] = proxy(emot["url"])
        emot["is_big_face"] = emot["emoticon_unique"].startswith("upower")

    content = message_to_str(event.message)

    await manager.send_message(
        event.room_id,
        WSMessage(
            type="danmaku",
            data=DanmakuData(
                time=int(event.time),
                username=event.sender.name,
                id=event.get_user_id(),
                content=content.strip(),
                emots=emots,
                reply_uname=event.reply_uname,
                medal=event.sender.medal,
                avatar=AVATAR_CACHE.get(event.get_user_id()),
            ),
        ),
    )


@matcher.handle()
async def handle_enter(event: UserEnterEvent, manager: WSManager):
    await manager.send_message(
        event.room_id,
        WSMessage(
            type="enter",
            data=EnterLeaveData(
                time=event.timestamp,
                username=event.uname,
                id=event.get_user_id(),
                avatar=AVATAR_CACHE.get(event.get_user_id()),
                medal=event.fans_medal,
            ),
        ),
    )


@matcher.handle()
async def handle_gift(event: SendGiftEvent, manager: WSManager):
    AVATAR_CACHE[event.get_user_id()] = proxy(event.face)
    await manager.send_message(
        event.room_id,
        WSMessage(
            type="gift",
            data=GiftData(
                time=event.timestamp,
                username=event.uname,
                id=event.get_user_id(),
                avatar=AVATAR_CACHE.get(event.get_user_id(), event.face),
                medal=event.medal,
                gift_name=event.gift_name,
                gift_num=event.num,
                price=event.price / 1000,
            ),
        ),
    )


@matcher.handle()
async def handle_super_chat(event: SuperChatEvent, manager: WSManager):
    AVATAR_CACHE[event.get_user_id()] = proxy(event.sender.face)
    await manager.send_message(
        event.room_id,
        WSMessage(
            type="superchat",
            data=SuperChatData(
                time=int(event.start_time),
                start_time=int(event.start_time),
                end_time=int(event.end_time),
                username=event.sender.name,
                id=event.get_user_id(),
                avatar=AVATAR_CACHE.get(event.get_user_id(), event.sender.face),
                medal=event.sender.medal,
                content=message_to_str(event.message).strip(),
                color=event.message_font_color,
                price=event.price,
            ),
        ),
    )


@matcher.handle()
async def handle_guard(event: GuardBuyEvent, manager: WSManager):
    AVATAR_CACHE[event.get_user_id()] = proxy(event.face)
    await manager.send_message(
        event.room_id,
        WSMessage(
            type="guard",
            data=GuardData(
                time=event.time,
                username=event.username,
                id=event.get_user_id(),
                avatar=AVATAR_CACHE.get(event.get_user_id(), event.face),
                medal=event.medal,
                guard_level=event.guard_level,
                price=event.price,
            ),
        ),
    )


@matcher.handle()
async def handle_like(event: LikeEvent, manager: WSManager):
    await manager.send_message(
        event.room_id,
        WSMessage(
            type="like",
            data=LikeData(
                time=int(time.time() * 1000),
                username=event.uname,
                id=event.get_user_id(),
                avatar=AVATAR_CACHE.get(event.get_user_id()),
                medal=event.fans_medal,
            ),
        ),
    )
