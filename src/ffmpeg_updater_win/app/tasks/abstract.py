import asyncio
import re
from abc import ABC, abstractmethod
from typing import ClassVar

from loguru import logger
from rich.panel import Panel

from ffmpeg_updater_win.app.clients.codex.abstract import BaseCodexFFAPIClient
from ffmpeg_updater_win.app.constants import CMD_FFMPEG_VERSION_ARG, FFMPEG_NUM_REGEX
from ffmpeg_updater_win.app.enums import FFSourceType, RequiredFfbinaryType
from ffmpeg_updater_win.app.models.config import UpdaterConfig
from ffmpeg_updater_win.app.utils import get_stdout, render_to_ansi


class BaseUpdaterTask[T: BaseCodexFFAPIClient](ABC):
    def __init__(self, api_client: T, settings: UpdaterConfig) -> None:
        self._log = logger
        self._log.debug('Initializing "{}"', self.__class__.__name__)
        self._api_client = api_client
        self._settings = settings

    async def run(self) -> None:
        try:
            await self._update()
        finally:
            await self._cleanup()

    async def _cleanup(self) -> None:
        await self._api_client.close_session()

    @abstractmethod
    async def _update(self) -> None:
        pass


class BaseFFmpegUpdaterTask(BaseUpdaterTask, ABC):
    TYPE: ClassVar[FFSourceType | None] = None

    @abstractmethod
    async def _perform_update(self) -> None:
        pass

    async def _update(self) -> None:
        """Update FFmpeg build."""
        self._log.info('Updating FFmpeg binaries from "{}"', self.TYPE)
        if await self._needs_update():
            await self._perform_update()
        else:
            self._log.info(
                'FFmpeg binaries are up-to-date in "{}", nothing to update',
                self._settings.destination,
            )

    async def _needs_update(self) -> bool:
        """Check if ffbinaries need to be updated."""
        if self._settings.force or not self._all_ffbinaries_exist():
            return True

        latest_version, local_version = await asyncio.gather(
            self._api_client.get_latest_version(), self._get_local_version()
        )
        self._log.info(
            'Local FFmpeg version "{}", latest version "{}"',
            local_version,
            latest_version,
        )
        if latest_version != local_version:
            self._log.info(
                'Local FFmpeg build version {} needs update to {}',
                local_version,
                latest_version,
            )
            return True
        return False

    def _all_ffbinaries_exist(self) -> bool:
        """Check whether all FFmpeg binaries exist on disk."""
        files = {path.name for path in self._settings.destination.iterdir()}
        return len(set(files) & RequiredFfbinaryType.choices()) == len(
            RequiredFfbinaryType
        )

    async def _get_local_version(self) -> str | None:
        """Get local FFmpeg build numerical build version."""
        bin_path = self._settings.destination / RequiredFfbinaryType.FFMPEG
        try:
            stdout = await get_stdout(
                cmd=(bin_path.as_posix(), CMD_FFMPEG_VERSION_ARG), log=self._log
            )
            panel = Panel(f'[blue]\n{stdout}', title='FFmpeg Version')
            self._log.debug(
                'Local FFmpeg build version:\n\n{}', render_to_ansi(renderable=panel)
            )
        except FileNotFoundError:
            self._log.warning(
                'Local FFmpeg build not found, will proceed with download'
            )
            return None
        except OSError as err:
            self._log.warning('Error getting local FFmpeg build version: "{}"', err)
            return None

        match = re.match(FFMPEG_NUM_REGEX, stdout)
        if not match:
            self._log.warning(
                'Error getting local FFmpeg build version using regex "{}"',
                FFMPEG_NUM_REGEX,
            )
            return None
        return match.group(1)
