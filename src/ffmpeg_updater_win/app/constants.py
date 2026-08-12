"""Constants module."""

from importlib.metadata import version as metadata_version
from pathlib import Path
from typing import Final

APP_NAME: Final[str] = 'ffmpeg-updater-win'
APP_VERSION: Final[str] = metadata_version(distribution_name=APP_NAME)

WINDOWS_PLATFORM: Final[str] = 'Windows'

DEFAULT_EXTRACT_PATH: Final[Path] = Path(r'C:\youtube-dl')

FFMPEG_NUM_REGEX: Final[str] = r'^ffmpeg\s+version\s+([\d\.]+)'
CMD_FFMPEG_VERSION_ARG: Final[str] = '-version'

CHUNK_SIZE: Final[int] = 1024 * 1024
