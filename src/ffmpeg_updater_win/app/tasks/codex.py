"""Codex/Gyan FFmpeg updater task."""

from typing import ClassVar, Literal

from ffmpeg_updater_win.app.core.zip_extractor import ZipStreamExtractor
from ffmpeg_updater_win.app.enums import FFSourceType, WinPlatformType
from ffmpeg_updater_win.app.tasks.abstract import BaseFFmpegUpdaterTask


class CodexFfmpegUpdaterTask(BaseFFmpegUpdaterTask):
    """Download the latest Codex essentials zip and extract FFmpeg binaries."""

    TYPE: ClassVar[Literal[FFSourceType.CODEX]] = FFSourceType.CODEX
    """Source identifier logged during the update."""

    def __init__(self, *args, **kwargs) -> None:
        """Create the zip stream extractor for this Codex update."""
        super().__init__(*args, **kwargs)
        self._stream_extractor = ZipStreamExtractor(settings=self._settings)

    async def _perform_update(self) -> None:
        """Stream the latest Codex zip into the destination directory."""
        if self._settings.platform is not WinPlatformType.WIN64:
            self._log.warning('Codex FFmpeg builds are only 64bit')
        await self._stream_extractor.process_zip_stream(
            self._api_client.download_latest_version()
        )
