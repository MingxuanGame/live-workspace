from __future__ import annotations

from collections.abc import Awaitable
from typing import Annotated, Any, Callable

from nonebot import get_plugin_config
from nonebot.log import logger
from nonebot.params import Depends
from pydantic import BaseModel

NotifierHandler = Callable[[dict[str, Any]], Awaitable[Any]]


class Config(BaseModel):
    notifier: str = ""


config = get_plugin_config(Config)


class Notifier:
    def __init__(self) -> None:
        self._handlers: dict[str, NotifierHandler] = {}

    async def emit(self, event: str, data: dict[str, Any]) -> None:
        event_handler = self._handlers.get(event)
        if event_handler is None:
            return
        await event_handler(data)

    def handle(self, event: str) -> Callable[[NotifierHandler], NotifierHandler]:
        def decorator(func: NotifierHandler) -> NotifierHandler:
            self._handlers[event] = func
            return func

        return decorator


class NotifierManager:
    def __init__(self) -> None:
        self.notifiers: dict[str, Notifier] = {}
        self.current_notifier = config.notifier

    async def emit(
        self, event: str, data: dict[str, Any], *, notifier: str = ""
    ) -> None:
        if not notifier:
            notifier = self.current_notifier
        notifier_instance = self.notifiers.get(notifier)
        if notifier_instance is None:
            return
        await notifier_instance.emit(event, data)


manager = NotifierManager()

BliveNotifier = Annotated[NotifierManager, Depends(lambda: manager)]


def register_notifier(name: str) -> Notifier:
    notifier = Notifier()
    manager.notifiers[name] = notifier
    logger.info(f"Registered notifier: {name}")
    return notifier
