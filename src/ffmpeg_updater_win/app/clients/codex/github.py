from typing import ClassVar, Literal

from ffmpeg_updater_win.app.clients.codex.abstract import BaseCodexFFAPIClient
from ffmpeg_updater_win.app.enums import (
    CodexArchExtensionType,
    CodexBuildType,
    CodexReleaseType,
)


class CodexFFGithubAPIClient(BaseCodexFFAPIClient):
    HOST: ClassVar[str] = 'https://github.com/GyanD/codexffmpeg'
    BUILDS_URL: ClassVar[str] = f'{HOST}/releases/download/{{tag}}/{{filename}}'
    LATEST_TAG_URL: ClassVar[str] = f'{HOST}/releases/latest'

    def _make_download_url(self, filename: str, build_version: str) -> str:
        return self.BUILDS_URL.format(tag=build_version, filename=filename)

    async def get_latest_version(self) -> str:
        return await self._get_latest_tag()

    async def _get_latest_tag(self) -> str:
        self._log.debug('GET {}', self.LATEST_TAG_URL)
        async with self._session.get(self.LATEST_TAG_URL) as response:
            return response.url.name

    @staticmethod
    def _make_archive_filename(
        release_type: CodexReleaseType,  # noqa: ARG004
        build_type: CodexBuildType,
        build_version: str,
        extension: Literal[CodexArchExtensionType.ZIP] = CodexArchExtensionType.ZIP,
    ) -> str:
        """Make zip archive filename to append to download url."""
        return f'ffmpeg-{build_version}-{build_type}_build.{extension}'
