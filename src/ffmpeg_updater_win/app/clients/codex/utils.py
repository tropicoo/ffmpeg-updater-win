from ffmpeg_updater_win.app.clients.codex.abstract import BaseCodexFFAPIClient
from ffmpeg_updater_win.app.clients.codex.mappings import CODEX_SOURCE_API_MAP
from ffmpeg_updater_win.app.models.config import UpdaterConfig
from ffmpeg_updater_win.app.tasks.abstract import BaseUpdaterTask
from ffmpeg_updater_win.app.tasks.codex import CodexFfmpegUpdaterTask


def get_api_cls(
    settings: UpdaterConfig, updater_task_cls: type[BaseUpdaterTask]
) -> type[BaseCodexFFAPIClient]:
    if issubclass(updater_task_cls, CodexFfmpegUpdaterTask):
        return CODEX_SOURCE_API_MAP[settings.codex_source]
    raise ValueError(f'Unknown updater task class "{updater_task_cls}"')
