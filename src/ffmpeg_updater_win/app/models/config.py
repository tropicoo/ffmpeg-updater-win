from pathlib import Path

from ffmpeg_updater_win.app.enums import (
    CodexSourceType,
    FFSourceType,
    LogLevelType,
    UpdaterComponentType,
    WinPlatformType,
)
from ffmpeg_updater_win.app.models.abstract import BaseStrictConfigModel


class UpdaterConfig(BaseStrictConfigModel):
    component: UpdaterComponentType
    destination: Path
    platform: WinPlatformType
    force: bool
    ffmpeg_source: FFSourceType
    codex_source: CodexSourceType
    verbose: LogLevelType
