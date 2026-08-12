from typing import ClassVar, Literal

from ffmpeg_updater_win.app.clients.codex.abstract import BaseCodexFFAPIClient
from ffmpeg_updater_win.app.enums import (
    CodexAPIPathType,
    CodexArchExtensionType,
    CodexBuildType,
    CodexReleaseType,
)


class CodexFFAPIClient(BaseCodexFFAPIClient):
    BUILDS_URL: ClassVar[str] = 'https://www.gyan.dev/ffmpeg/builds/'
    _TYPE_MAP: ClassVar[dict[CodexReleaseType, str]] = {
        CodexReleaseType.RELEASE: BUILDS_URL + CodexAPIPathType.LATEST_RELEASE_VER,
        CodexReleaseType.GIT: BUILDS_URL + CodexAPIPathType.LATEST_GIT_VER,
    }

    async def get_changelog_counter(self) -> str:
        return await self._get_text(
            self.BUILDS_URL + CodexAPIPathType.CHANGELOG_COUNTER
        )

    async def get_latest_version(
        self, release_type: CodexReleaseType = CodexReleaseType.RELEASE
    ) -> str:
        return await self._get_text(self._TYPE_MAP[release_type])

    async def get_last_build_date(self) -> str:
        return await self._get_text(
            self.BUILDS_URL + CodexAPIPathType.LAST_BUILD_UPDATE
        )

    async def get_next_build_date(self) -> str:
        return await self._get_text(
            self.BUILDS_URL + CodexAPIPathType.NEXT_BUILD_UPDATE
        )

    def _make_download_url(self, filename: str, build_version: str) -> str:  # noqa: ARG002
        return self.BUILDS_URL + filename

    @staticmethod
    def _make_archive_filename(
        release_type: CodexReleaseType,
        build_type: CodexBuildType,
        build_version: str,  # noqa: ARG004
        extension: Literal[CodexArchExtensionType.ZIP] = CodexArchExtensionType.ZIP,
    ) -> str:
        """Make zip archive filename to append to download url."""
        return f'ffmpeg-{release_type}-{build_type}.{extension}'
