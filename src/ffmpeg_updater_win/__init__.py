"""FFmpeg binaries updater package for Windows."""

from typing import Final

from ffmpeg_updater_win.app.constants import APP_VERSION
from ffmpeg_updater_win.main import main

__version__: Final[str] = APP_VERSION
"""Installed package version string."""

__all__: Final[list[str]] = ['__version__', 'main']
"""Public package exports."""
