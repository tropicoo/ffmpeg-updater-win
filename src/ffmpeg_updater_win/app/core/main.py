import asyncio

from loguru import logger

from ffmpeg_updater_win.app.banner import BANNER
from ffmpeg_updater_win.app.core.ffmpeg_updater import FFmpegUpdater
from ffmpeg_updater_win.app.log import init_logging
from ffmpeg_updater_win.app.models.config import UpdaterConfig
from ffmpeg_updater_win.app.utils import rich_console


def main_start(updater_config: UpdaterConfig) -> None:
    init_logging(log_level=updater_config.verbose)
    rich_console.print(BANNER)

    logger.info('Starting main app')
    try:
        asyncio.run(FFmpegUpdater(config=updater_config).run())
    finally:
        logger.info('Exiting main app')
