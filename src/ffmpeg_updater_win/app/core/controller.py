"""Synchronous entrypoint that runs the async updater."""

import asyncio

import typer
from loguru import logger

from ffmpeg_updater_win.app.banner import BANNER
from ffmpeg_updater_win.app.core.ffmpeg_updater import FFmpegUpdater
from ffmpeg_updater_win.app.enums import ExitCodeType
from ffmpeg_updater_win.app.utils import rich_console


class MainAppController:
    """Print the banner and drive a single updater run."""

    def __init__(self, updater: FFmpegUpdater) -> None:
        """Store the updater instance to run."""
        self._updater = updater

    def run(self) -> None:
        """Start the updater event loop and exit with code 1 if the update fails."""
        rich_console.print(BANNER)
        logger.info('Starting main app')
        try:
            asyncio.run(self._updater.run())
        except Exception:
            logger.exception('Update failed')
            raise typer.Exit(code=ExitCodeType.EXIT_ERROR) from None
        finally:
            logger.info('Exiting main app')
