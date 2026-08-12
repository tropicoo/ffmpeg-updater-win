from pathlib import Path

from pydantic import ConfigDict

from ffmpeg_updater_win.app.enums import (
    CodexSourceType,
    FFSourceType,
    LogLevelType,
    UpdaterComponentType,
    WinPlatformType,
)
from ffmpeg_updater_win.app.models.abstract import BaseStrictConfigModel


class UpdaterConfig(BaseStrictConfigModel):
    model_config = ConfigDict(
        strict=True, frozen=True, extra='forbid', arbitrary_types_allowed=True
    )

    component: UpdaterComponentType
    destination: Path
    platform: WinPlatformType
    force: bool
    ffmpeg_source: FFSourceType
    codex_source: CodexSourceType
    verbose: LogLevelType
