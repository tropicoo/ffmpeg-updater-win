"""Runtime configuration models."""

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
    """CLI-derived settings for an updater run."""

    component: UpdaterComponentType
    """Component to update (currently FFmpeg only)."""

    destination: Path
    """Directory where binaries are extracted."""

    platform: WinPlatformType
    """Requested Windows architecture."""

    force: bool
    """Skip the local version check and always download."""

    ffmpeg_source: FFSourceType
    """FFmpeg build provider (currently Codex only)."""

    codex_source: CodexSourceType
    """Where to fetch Codex builds: GitHub releases or gyan.dev."""

    verbose: LogLevelType
    """Log verbosity mapped from the `--verbose` flag."""
