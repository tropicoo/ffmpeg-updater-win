from typing import Final

from ffmpeg_updater_win.app.clients.codex.abstract import BaseCodexFFAPIClient
from ffmpeg_updater_win.app.clients.codex.codex import CodexFFAPIClient
from ffmpeg_updater_win.app.clients.codex.github import CodexFFGithubAPIClient
from ffmpeg_updater_win.app.enums import CodexSourceType

CODEX_SOURCE_API_MAP: Final[dict[CodexSourceType, type[BaseCodexFFAPIClient]]] = {
    CodexSourceType.CODEX: CodexFFAPIClient,
    CodexSourceType.GITHUB: CodexFFGithubAPIClient,
}
