"""Logging configuration."""

import sys

from loguru import logger

from ffmpeg_updater_win.app.enums import LogLevelType


def init_logging(log_level: LogLevelType) -> None:
    """Configure Loguru to write colorized messages to stderr."""
    logger.remove()
    logger.add(
        sys.stderr,
        colorize=True,
        level=log_level.name,
        format=(
            '<green>{time:YYYY-MM-DD HH:mm:ss}</green> | '
            '<level>{level:<8}</level> | '
            '<cyan>{module:<15}</cyan><cyan>{function:<24}</cyan>:<magenta>{line:>4}</magenta> | '
            '<level>{message}</level>'
        ),
    )
