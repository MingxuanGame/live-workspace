"""弹幕事件模型定义"""

from __future__ import annotations

from typing import Literal

from nonebot.adapters.bilibili_live import Medal
from nonebot.adapters.bilibili_live.message import Emoticon
from pydantic import BaseModel


class ExtendedEmoticon(Emoticon):
    """扩展表情数据模型"""

    is_big_face: bool


class DanmakuData(BaseModel):
    """弹幕消息数据"""

    time: int  # 时间戳，单位毫秒
    username: str
    id: str  # 用户ID（uid或openid）
    content: str
    color: str | None = None  # 弹幕颜色，默认为白
    font_size: int | None = None  # 弹幕字体大小，默认为25
    emots: list[ExtendedEmoticon] | None = None  # 表情列表
    reply_uname: str | None = None  # 被回复的用户名
    medal: Medal | None = None  # 粉丝牌信息
    avatar: str | None = None  # 头像URL


class EnterLeaveData(BaseModel):
    """进场/离场消息数据"""

    time: int
    username: str
    id: str
    avatar: str | None = None
    medal: Medal | None = None


class GiftData(BaseModel):
    """礼物消息数据"""

    time: int
    username: str
    id: str
    avatar: str | None = None
    medal: Medal | None = None
    gift_name: str
    gift_num: int
    price: float  # 礼物单价，单位为RMB


class SuperChatData(BaseModel):
    """醒目留言数据"""

    time: int
    start_time: int  # 超级留言开始时间戳
    end_time: int  # 超级留言结束时间戳
    username: str
    id: str
    content: str
    color: str | None = None
    font_size: int | None = None
    medal: Medal | None = None
    price: float  # 超级留言价格，单位为RMB
    avatar: str | None = None


class GuardData(BaseModel):
    """上舰消息数据"""

    time: int
    username: str
    id: str
    avatar: str
    medal: Medal | None = None
    guard_level: int  # 1:总督, 2:提督, 3:舰长
    price: float


class LikeData(BaseModel):
    """点赞消息数据"""

    time: int
    username: str
    id: str
    avatar: str | None = None
    medal: Medal | None = None


# 消息类型
MessageType = Literal["danmaku", "enter", "leave", "gift", "superchat", "guard", "like"]


class WSMessage(BaseModel):
    """WebSocket 消息结构"""

    type: MessageType
    data: DanmakuData | EnterLeaveData | GiftData | SuperChatData | GuardData | LikeData
