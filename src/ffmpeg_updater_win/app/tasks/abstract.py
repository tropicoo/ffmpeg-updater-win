"""Abstract updater tasks and FFmpeg version checks."""

import asyncio
from abc import ABC, abstractmethod
from typing import ClassVar

from loguru import logger
from rich.panel import Panel

from ffmpeg_updater_win.app.clients.codex.abstract import BaseCodexFFAPIClient
from ffmpeg_updater_win.app.constants import FFMPEG_VERSION_ARG, FFMPEG_VERSION_RE
from ffmpeg_updater_win.app.enums import FFSourceType, RequiredFfbinaryType
from ffmpeg_updater_win.app.models.config import UpdaterConfig
from ffmpeg_updater_win.app.utils import get_stdout, render_to_ansi


class BaseUpdaterTask[T: BaseCodexFFAPIClient](ABC):
    """Run an update against an HTTP client and always close the session."""

    def __init__(self, api_client: T, settings: UpdaterConfig) -> None:
        """Store the API client and updater settings."""
        self._log = logger
        self._log.debug('Initializing "{}"', self.__class__.__name__)
        self._api_client = api_client
        self._settings = settings

    async def run(self) -> None:
        """Execute the update and close the HTTP session afterwards."""
        try:
            await self._update()
        finally:
            await self._cleanup()

    async def _cleanup(self) -> None:
        """Close the API client session."""
        await self._api_client.close_session()

    @abstractmethod
    async def _update(self) -> None:
        """Perform the source-specific update."""


class BaseFFmpegUpdaterTask(BaseUpdaterTask, ABC):
    """FFmpeg updater that skips download when local binaries are current."""

    TYPE: ClassVar[FFSourceType | None] = None
    """FFmpeg source this task knows how to update."""

    @abstractmethod
    async def _perform_update(self) -> None:
        """Download and extract binaries when an update is required."""

    async def _update(self) -> None:
        """Update FFmpeg binaries when the local build is missing or outdated."""
        self._log.info('Updating FFmpeg binaries from "{}"', self.TYPE)
        if await self._needs_update():
            await self._perform_update()
        else:
            self._log.info(
                'FFmpeg binaries are up-to-date in "{}", nothing to update',
                self._settings.destination,
            )

    async def _needs_update(self) -> bool:
        """Return whether local binaries should be replaced."""
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
        """Return whether all required FFmpeg binaries exist on disk."""
        files = {path.name for path in self._settings.destination.iterdir()}
        return len(set(files) & RequiredFfbinaryType.choices()) == len(
            RequiredFfbinaryType
        )

    async def _get_local_version(self) -> str | None:
        """Return the local FFmpeg numeric version, or None if it cannot be read."""
        bin_path = self._settings.destination / RequiredFfbinaryType.FFMPEG
        try:
            stdout = await get_stdout(
                cmd=(bin_path.as_posix(), FFMPEG_VERSION_ARG), log=self._log
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

        match = FFMPEG_VERSION_RE.match(stdout)
        if not match:
            self._log.warning(
                'Error getting local FFmpeg build version using regex "{}"',
                FFMPEG_VERSION_RE.pattern,
            )
            return None
        return match.group(1)
