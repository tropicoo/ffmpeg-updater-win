"""Codex FFmpeg client that downloads GitHub release zips."""

from typing import ClassVar, Literal

from ffmpeg_updater_win.app.clients.codex.abstract import BaseCodexFFAPIClient
from ffmpeg_updater_win.app.enums import (
    CodexArchExtensionType,
    CodexBuildType,
    CodexReleaseType,
)


class CodexFFGithubAPIClient(BaseCodexFFAPIClient):
    """Fetch Codex archives from the `GyanD/codexffmpeg` GitHub releases."""

    HOST: ClassVar[str] = 'https://github.com/GyanD/codexffmpeg'
    """GitHub repository URL for Codex FFmpeg releases."""

    BUILDS_URL: ClassVar[str] = f'{HOST}/releases/download/{{tag}}/{{filename}}'
    """Download URL template with `{tag}` and `{filename}` placeholders."""

    LATEST_TAG_URL: ClassVar[str] = f'{HOST}/releases/latest'
    """GitHub URL that redirects to the latest release tag."""

    def _make_download_url(self, filename: str, build_version: str) -> str:
        """Return the GitHub release-asset download URL."""
        return self.BUILDS_URL.format(tag=build_version, filename=filename)

    async def get_latest_version(self) -> str:
        """Return the latest GitHub release tag name."""
        return await self._get_latest_tag()

    async def _get_latest_tag(self) -> str:
        """Follow `/releases/latest` and return the redirected tag."""
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
        """Build the GitHub release zip filename for a versioned Codex build."""
        return f'ffmpeg-{build_version}-{build_type}_build.{extension}'
