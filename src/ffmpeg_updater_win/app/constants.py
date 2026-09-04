"""Shared application constants."""

import re
from importlib.metadata import version as metadata_version
from pathlib import Path
from typing import Final

APP_NAME: Final[str] = 'ffmpeg-updater-win'
"""PyPI / CLI distribution name used for metadata lookup."""

APP_VERSION: Final[str] = metadata_version(distribution_name=APP_NAME)
"""Installed package version from importlib metadata."""

WINDOWS_PLATFORM: Final[str] = 'Windows'
"""`platform.system()` value required to run this application."""

DEFAULT_EXTRACT_PATH: Final[Path] = Path(r'C:\youtube-dl')
"""Default directory where FFmpeg executables are written."""

FFMPEG_VERSION_RE: Final[re.Pattern[str]] = re.compile(r'^ffmpeg\s+version\s+([\d\.]+)')
"""Pattern that captures the numeric FFmpeg version from `-version` stdout."""

FFMPEG_VERSION_ARG: Final[str] = '-version'
"""CLI argument passed to FFmpeg binaries to print version information."""

CHUNK_SIZE: Final[int] = 1024 * 1024
"""HTTP download chunk size in bytes."""
