from __future__ import annotations

import asyncio

from src.lib.fakebot import FAKE_BOT
from src.lib.http import get_http_client

from .config import Config
from .model import (
    BPM as BPM,
    PP as PP,
    AccuracyPerformance as AccuracyPerformance,
    Audio as Audio,
    Background as Background,
    BanchoStatus as BanchoStatus,
    Beatmap as Beatmap,
    BeatmapObjects as BeatmapObjects,
    BeatmapStats as BeatmapStats,
    BeatmapStatus as BeatmapStatus,
    BeatmapTime as BeatmapTime,
    ChatVisibilityStatus as ChatVisibilityStatus,
    Client as Client,
    Combo as Combo,
    CountryCode as CountryCode,
    Cursor as Cursor,
    DirectPath as DirectPath,
    Files as Files,
    Folders as Folders,
    FruitsKeybinds as FruitsKeybinds,
    Graph as Graph,
    Group as Group,
    HealthBar as HealthBar,
    Hits as Hits,
    Keybinds as Keybinds,
    Leaderboard as Leaderboard,
    LeaderboardType as LeaderboardType,
    Mania as Mania,
    Mode as Mode,
    Mods as Mods,
    Mouse as Mouse,
    Offset as Offset,
    OsuKeybinds as OsuKeybinds,
    Performance as Performance,
    Play as Play,
    Points as Points,
    PPDetailed as PPDetailed,
    Profile as Profile,
    ProgressBar as ProgressBar,
    Rank as Rank,
    Resolution as Resolution,
    ResultsScreen as ResultsScreen,
    ResultsScreenHits as ResultsScreenHits,
    ResultsScreenPP as ResultsScreenPP,
    ScoreMeter as ScoreMeter,
    ScoreMeterType as ScoreMeterType,
    ScrollDirection as ScrollDirection,
    Session as Session,
    Settings as Settings,
    Skin as Skin,
    Sort as Sort,
    Stars as Stars,
    State as State,
    Status as Status,
    StatValue as StatValue,
    Tablet as Tablet,
    TaikoKeybinds as TaikoKeybinds,
    Team as Team,
    TosuData as TosuData,
    TosuEvent as TosuEvent,
    TotalScore as TotalScore,
    Tourney as Tourney,
    TourneyClient as TourneyClient,
    TourneyUser as TourneyUser,
    UserStatus as UserStatus,
    Volume as Volume,
)

from aiohttp import ClientError
from nonebot import get_plugin_config, logger
from nonebot.compat import type_validate_python
from nonebot.message import handle_event

_config = get_plugin_config(Config)
tasks = set()


async def _loop():
    attempts = 0
    while True:
        next_reconnect_delay = _config.tosu_reconnect_base_delay * (2**attempts)
        try:
            session = get_http_client()
            async with session.ws_connect(
                f"ws://{_config.tosu_host}:{_config.tosu_port}/websocket/v2"
            ) as ws:
                logger.success("Connected to Tosu WebSocket server.")
                while True:
                    msg = await ws.receive_json()
                    task = asyncio.create_task(
                        handle_event(FAKE_BOT, type_validate_python(TosuEvent, msg))
                    )
                    tasks.add(task)
                    task.add_done_callback(tasks.discard)
        except (ClientError, ConnectionError) as e:
            logger.warning(
                f"Connecting to Tosu WebSocket server "
                f"failed: {e}, Reconnect in {next_reconnect_delay} seconds",
            )
        except Exception:
            logger.exception(
                "Unexpected error when connecting to Tosu WebSocket server."
                f"Reconnect in {next_reconnect_delay} seconds"
            )
        await asyncio.sleep(next_reconnect_delay)
        attempts += 1
        if attempts > _config.tosu_reconnect_max_attempts:
            logger.error(
                f"Failed to connect to Tosu WebSocket server after "
                f"{_config.tosu_reconnect_max_attempts} attempts. "
                "Will stop trying to reconnect."
            )
            break


async def start_tosu_websocket():
    task = asyncio.create_task(_loop())
    task.add_done_callback(tasks.discard)
    tasks.add(task)


async def stop_tosu_websocket():
    for task in tasks:
        task.cancel()
    tasks.clear()
    logger.info("Tosu WebSocket tasks cancelled.")
