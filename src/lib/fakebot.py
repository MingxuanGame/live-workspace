from __future__ import annotations

from typing import Any, override

from nonebot import get_driver
from nonebot.adapters import Adapter, Bot


class FakeAdapter(Adapter):
    @override
    @classmethod
    def get_name(cls) -> str:
        return "Fake"

    @override
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        pass


FAKE_ADAPTER = FakeAdapter(get_driver())


class FakeBot(Bot):
    def __init__(self):
        super().__init__(self_id="fake_bot", adapter=FAKE_ADAPTER)

    @override
    async def send(self, *args, **kwargs):
        pass


FAKE_BOT = FakeBot()
