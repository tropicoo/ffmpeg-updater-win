"""Abstract HTTP client for Codex FFmpeg zip downloads."""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import ClassVar, Literal

from aiohttp import ClientSession, TCPConnector
from loguru import logger

from ffmpeg_updater_win.app.constants import CHUNK_SIZE
from ffmpeg_updater_win.app.enums import (
    CodexArchExtensionType,
    CodexBuildType,
    CodexReleaseType,
)
from ffmpeg_updater_win.app.third_party.stream_unzip import stream_unzip


class BaseCodexFFAPIClient(ABC):
    """Download and stream-unzip Codex FFmpeg archives."""

    BUILDS_URL: ClassVar[str | None] = None
    """Base URL used to construct download links."""

    def __init__(self) -> None:
        """Create an aiohttp session for Codex requests."""
        self._log = logger
        self._log.debug('Initializing "{}"', self.__class__.__name__)
        self._session = ClientSession(
            connector=TCPConnector(verify_ssl=False), raise_for_status=True
        )

    async def _get_text(self, url: str) -> str:
        """Return response body text from a GET request."""
        self._log.debug('GET {}', url)
        async with self._session.get(url) as response:
            return await response.text()

    async def close_session(self) -> None:
        """Close the aiohttp client session."""
        self._log.debug('Close client session')
        await self._session.close()

    async def download_latest_version(
        self,
        release_type: Literal[CodexReleaseType.RELEASE] = CodexReleaseType.RELEASE,
        build_type: Literal[CodexBuildType.ESSENTIALS] = CodexBuildType.ESSENTIALS,
    ) -> AsyncGenerator[tuple[bytes, int, AsyncGenerator[bytes, None]], None]:
        """Yield unzipped zip members for the latest matching Codex archive."""
        latest = await self.get_latest_version()
        self._log.info('Latest version: "{}"', latest)

        async def zipped_chunks_generator() -> AsyncGenerator[bytes, None]:
            """Yield raw zip archive bytes as they are downloaded."""
            zip_filename = self._make_archive_filename(
                release_type=release_type,
                build_type=build_type,
                build_version=latest,
            )
            url = self._make_download_url(filename=zip_filename, build_version=latest)
            self._log.debug('GET {}', url)
            self._log.debug('Start download {}', zip_filename)
            async with self._session.get(url) as response:
                async for chunk in response.content.iter_chunked(CHUNK_SIZE):
                    yield chunk
                self._log.debug('End download {}', zip_filename)

        async for filename, file_size, unzipped_chunks in stream_unzip(
            zipped_chunks_generator()
        ):
            yield filename, file_size, unzipped_chunks

    @staticmethod
    @abstractmethod
    def _make_archive_filename(
        release_type: CodexReleaseType,
        build_type: CodexBuildType,
        build_version: str,
        extension: Literal[CodexArchExtensionType.ZIP] = CodexArchExtensionType.ZIP,
    ) -> str:
        """Build the zip filename to append to the download URL."""

    @abstractmethod
    def _make_download_url(self, filename: str, build_version: str) -> str:
        """Return the absolute download URL for an archive filename."""

    @abstractmethod
    async def get_latest_version(self, *args, **kwargs) -> str:
        """Return the latest published version string for this source."""
