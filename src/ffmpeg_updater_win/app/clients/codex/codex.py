"""Codex FFmpeg client that downloads archives from gyan.dev."""

from typing import ClassVar, Literal

from ffmpeg_updater_win.app.clients.codex.abstract import BaseCodexFFAPIClient
from ffmpeg_updater_win.app.enums import (
    CodexAPIPathType,
    CodexArchExtensionType,
    CodexBuildType,
    CodexReleaseType,
)


class CodexFFAPIClient(BaseCodexFFAPIClient):
    """Fetch Codex version metadata and rolling zip names from gyan.dev."""

    BUILDS_URL: ClassVar[str] = 'https://www.gyan.dev/ffmpeg/builds/'
    """Root URL of the Gyan FFmpeg builds site."""

    _TYPE_MAP: ClassVar[dict[CodexReleaseType, str]] = {
        CodexReleaseType.RELEASE: BUILDS_URL + CodexAPIPathType.LATEST_RELEASE_VER,
        CodexReleaseType.GIT: BUILDS_URL + CodexAPIPathType.LATEST_GIT_VER,
    }
    """Release channel to plain-text version endpoint."""

    async def get_changelog_counter(self) -> str:
        """Return the site changelog counter."""
        return await self._get_text(
            self.BUILDS_URL + CodexAPIPathType.CHANGELOG_COUNTER
        )

    async def get_latest_version(
        self, release_type: CodexReleaseType = CodexReleaseType.RELEASE
    ) -> str:
        """Return the latest version string for a Codex release channel."""
        return await self._get_text(self._TYPE_MAP[release_type])

    async def get_last_build_date(self) -> str:
        """Return the timestamp of the last published build."""
        return await self._get_text(
            self.BUILDS_URL + CodexAPIPathType.LAST_BUILD_UPDATE
        )

    async def get_next_build_date(self) -> str:
        """Return the timestamp of the next expected build."""
        return await self._get_text(
            self.BUILDS_URL + CodexAPIPathType.NEXT_BUILD_UPDATE
        )

    def _make_download_url(self, filename: str, build_version: str) -> str:  # noqa: ARG002
        """Return the gyan.dev URL for a rolling archive filename."""
        return self.BUILDS_URL + filename

    @staticmethod
    def _make_archive_filename(
        release_type: CodexReleaseType,
        build_type: CodexBuildType,
        build_version: str,  # noqa: ARG004
        extension: Literal[CodexArchExtensionType.ZIP] = CodexArchExtensionType.ZIP,
    ) -> str:
        """Build the rolling gyan.dev zip filename (version is not in the name)."""
        return f'ffmpeg-{release_type}-{build_type}.{extension}'
