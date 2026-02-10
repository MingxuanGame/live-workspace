from __future__ import annotations

from typing import TypedDict, cast

from nonebot import get_driver, get_loaded_plugins


class Command(TypedDict):
    name: str
    description: str
    usage: str


METADATA_KEY = "danmaku_commands"

driver = get_driver()
commands: dict[str, Command] = {}


@driver.on_startup
async def startup():
    global commands
    for plugin in get_loaded_plugins():
        metadata = plugin.metadata
        if metadata and metadata.extra and METADATA_KEY in metadata.extra:
            for cmd in metadata.extra[METADATA_KEY]:
                if cmd["name"] in commands:
                    driver.logger.warning(
                        f"Command '{cmd['name']}' from plugin '{plugin.name}' "
                        f"conflicts with an existing command. Skipping."
                    )
                    continue
                commands[cmd["name"]] = cast(Command, cmd)
