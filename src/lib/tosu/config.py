from __future__ import annotations

from pydantic import BaseModel


class Config(BaseModel):
    tosu_host: str = "127.0.0.1"
    tosu_port: int = 24050
    tosu_reconnect_base_delay: int = 2
    tosu_reconnect_max_attempts: int = 5
