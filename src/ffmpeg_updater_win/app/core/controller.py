import asyncio

from loguru import logger

from ffmpeg_updater_win.app.banner import BANNER
from ffmpeg_updater_win.app.core.ffmpeg_updater import FFmpegUpdater
from ffmpeg_updater_win.app.utils import rich_console


class MainAppController:
    def __init__(self, updater: FFmpegUpdater) -> None:
        self._updater = updater

    def run(self) -> None:
        rich_console.print(BANNER)
        logger.info('Starting main app')
        try:
            asyncio.run(self._updater.run())
        finally:
            logger.info('Exiting main app')
