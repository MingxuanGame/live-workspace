from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Annotated

from .commands import commands
from .config import config
from .models import WSMessage

from aiohttp import ClientSession
from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from nonebot import get_driver
from nonebot.internal.params import Depends

app = FastAPI()

# 前端静态文件目录
DEV_FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "dist"
PROD_FRONTEND_DIR = Path(__file__).parent / "frontend" / "dist"

PROXY_TTL = 60 * 60  # 1小时
PROXY_CACHE = {}  # url -> (content, content_type, timestamp)

driver = get_driver()


def get_frontend_dir() -> Path | None:
    """获取前端构建目录"""
    if config.debug and DEV_FRONTEND_DIR.exists():
        return DEV_FRONTEND_DIR

    if PROD_FRONTEND_DIR.exists():
        return PROD_FRONTEND_DIR
    if DEV_FRONTEND_DIR.exists():
        return DEV_FRONTEND_DIR
    return None


@app.get("/proxy/{url:path}")
async def assets_proxy(url: str):
    """代理请求，解决前端跨域问题"""
    # 检查缓存
    cached = PROXY_CACHE.get(url)
    if cached and (asyncio.get_event_loop().time() - cached[2] < PROXY_TTL):
        return Response(cached[0], media_type=cached[1])

    async with ClientSession() as session, session.get(url) as response:
        content = await response.read()
        PROXY_CACHE[url] = (
            content,
            response.headers.get("Content-Type"),
            asyncio.get_event_loop().time(),
        )
        return Response(content, media_type=response.headers.get("Content-Type"))


@app.get("/commands")
async def get_commands():
    """返回所有可用的命令"""
    return {
        "commands": {
            name: cmd
            for name, cmd in commands.items()
            if not callable(cmd["enabled"]) or cmd["enabled"]()
        },
        "prefix": driver.config.command_start,
    }


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    """WebSocket 端点，用于接收弹幕"""
    await manager.connect(room_id, websocket)
    try:
        while True:
            # 保持连接，等待客户端消息（心跳等）
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(room_id, websocket)
    except Exception:
        await manager.disconnect(room_id, websocket)


# 挂载静态文件（如果存在构建目录）
if PROD_FRONTEND_DIR.exists() or DEV_FRONTEND_DIR.exists():
    FRONTEND_DIR = PROD_FRONTEND_DIR if PROD_FRONTEND_DIR.exists() else DEV_FRONTEND_DIR

    # 挂载静态资源（js, css, 图片等）
    assets_dir = FRONTEND_DIR / "assets"
    if assets_dir.exists():
        app.mount(
            "/assets",
            StaticFiles(directory=str(assets_dir)),
            name="danmaku_assets",
        )

    @app.get("/")
    async def serve_danmaku_index():
        """返回弹幕页面"""
        index_file = FRONTEND_DIR / "index.html"
        if index_file.exists():
            return FileResponse(index_file, media_type="text/html")
        return {"error": "Frontend not built"}

    # 处理前端路由（SPA fallback）
    @app.get("/{path:path}")
    async def serve_danmaku_spa(path: str):
        """SPA 路由回退"""
        # 尝试直接返回文件
        file_path = FRONTEND_DIR / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        # 否则返回 index.html（SPA 路由）
        index_file = FRONTEND_DIR / "index.html"
        if index_file.exists():
            return FileResponse(index_file, media_type="text/html")
        return {"error": "Frontend not built"}


class ConnectionManager:
    """管理 WebSocket 连接"""

    def __init__(self):
        # room_id -> set[WebSocket]
        self._connections: dict[int, set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, room_id: int, websocket: WebSocket) -> None:
        """添加连接到房间"""
        await websocket.accept()
        async with self._lock:
            if room_id not in self._connections:
                self._connections[room_id] = set()
            self._connections[room_id].add(websocket)

    async def disconnect(self, room_id: int, websocket: WebSocket) -> None:
        """从房间移除连接"""
        async with self._lock:
            if room_id in self._connections:
                self._connections[room_id].discard(websocket)
                if not self._connections[room_id]:
                    del self._connections[room_id]

    def get_connections(self, room_id: int) -> set[WebSocket]:
        """获取房间的所有连接"""
        return self._connections.get(room_id, set()).copy()

    def get_room_ids(self) -> set[int]:
        """获取所有房间ID"""
        return set(self._connections.keys())

    def get_connection_count(self, room_id: int) -> int:
        """获取房间连接数"""
        return len(self._connections.get(room_id, set()))

    def get_total_connections(self) -> int:
        """获取总连接数"""
        return sum(len(conns) for conns in self._connections.values())

    async def send_message(self, room_id: int, message: WSMessage) -> None:
        """发送消息到房间的所有连接"""
        connections = self.get_connections(room_id)
        for websocket in connections:
            await websocket.send_text(message.model_dump_json())


# 全局连接管理器实例
manager = ConnectionManager()
WSManager = Annotated[ConnectionManager, Depends(lambda: manager)]
