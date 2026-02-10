"""Hatch build hook for building frontend."""  # noqa: INP001

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    """Build hook to compile frontend before packaging."""

    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:  # noqa: ARG002
        """Build frontend and copy dist to package directory."""
        root = Path(self.root)
        frontend_dir = root / "frontend"
        source_dist = frontend_dir / "dist"
        target_dist = root / "nonebot_plugin_danmaku" / "frontend" / "dist"

        # 检查前端目录是否存在
        if not frontend_dir.exists():
            self.app.display_warning("Frontend directory not found, skipping build")
            return

        # 检查是否有 package.json
        package_json = frontend_dir / "package.json"
        if not package_json.exists():
            self.app.display_warning("package.json not found, skipping frontend build")
            return

        self.app.display_info("Building frontend...")

        # 安装依赖
        try:
            subprocess.run(
                ["pnpm", "install"],  # noqa: S607
                cwd=frontend_dir,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            self.app.display_error(f"Failed to install dependencies: {e.stderr}")
            raise
        except FileNotFoundError:
            self.app.display_error("pnpm not found, please install pnpm first")
            raise

        # 构建前端
        try:
            subprocess.run(
                ["pnpm", "run", "build"],  # noqa: S607
                cwd=frontend_dir,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            self.app.display_error(f"Failed to build frontend: {e.stderr}")
            raise

        # 检查 dist 目录是否生成
        if not source_dist.exists():
            self.app.display_error("Frontend build did not produce dist directory")
            raise RuntimeError("Frontend build failed")

        # 清理目标目录
        if target_dist.exists():
            shutil.rmtree(target_dist)

        # 复制 dist 到包目录
        target_dist.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_dist, target_dist)

        self.app.display_success(f"Frontend built and copied to {target_dist}")
