"""FFmpeg Updater module."""

import asyncio

from loguru import logger

from ffmpeg_updater_win.app.constants import APP_VERSION
from ffmpeg_updater_win.app.exceptions import FFmpegUpdaterError
from ffmpeg_updater_win.app.models.config import UpdaterConfig
from ffmpeg_updater_win.app.tasks.managers import TaskManager


class FFmpegUpdater:
    """Main FFmpeg FFmpegUpdater Class."""

    def __init__(self, config: UpdaterConfig) -> None:
        self._log = logger
        self._log.info(
            'Initializing "{}" version {}', self.__class__.__name__, APP_VERSION
        )
        self._conf = config
        self._task_manager = TaskManager(settings=self._conf)

    async def run(self) -> None:
        """Start update tasks."""
        self._log.info('Starting{} update', ' force' if self._conf.force else '')
        self._check_destination_path_existence()
        await asyncio.gather(*self._task_manager.create_tasks(), return_exceptions=True)
        self._log.info('{}pdate finished', 'Force u' if self._conf.force else 'U')

    def _check_destination_path_existence(self) -> None:
        """Check if destination path exists and is a directory."""
        path = self._conf.destination
        if not path.exists():
            self._log.info('Creating destination directory "{}"', path)
            path.mkdir(parents=True)
            return

        if not path.is_dir():
            raise FFmpegUpdaterError(f'{path} is not a directory')
