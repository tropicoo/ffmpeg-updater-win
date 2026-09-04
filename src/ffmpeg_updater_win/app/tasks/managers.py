"""Factory that turns config into runnable updater tasks."""

from asyncio import Task
from typing import ClassVar

from loguru import logger

from ffmpeg_updater_win.app.clients.codex.abstract import BaseCodexFFAPIClient
from ffmpeg_updater_win.app.clients.codex.utils import get_api_cls
from ffmpeg_updater_win.app.enums import UpdaterComponentType
from ffmpeg_updater_win.app.models.config import UpdaterConfig
from ffmpeg_updater_win.app.tasks.abstract import BaseUpdaterTask
from ffmpeg_updater_win.app.tasks.codex import CodexFfmpegUpdaterTask
from ffmpeg_updater_win.app.utils import create_task


class TaskManager:
    """Create asyncio tasks for the selected updater component."""

    TASKS: ClassVar[dict[UpdaterComponentType, tuple[type[BaseUpdaterTask], ...]]] = {
        UpdaterComponentType.FFMPEG: (CodexFfmpegUpdaterTask,),
    }
    """Component-to-task-class registry."""

    def __init__(self, settings: UpdaterConfig) -> None:
        """Store updater settings used when creating tasks."""
        self._log = logger
        self._log.debug('Initializing "{}"', self.__class__.__name__)
        self._settings = settings

    def create_tasks(self) -> list[Task]:
        """Build and schedule updater tasks for the configured component."""
        return [
            create_task(
                task_cls(
                    settings=self._settings,
                    api_client=self._create_api_client(task_cls=task_cls),
                ).run(),
                log=self._log,
                task_name=task_cls.__name__,
                exception_message='Task {} raised an exception',
                exception_message_args=(task_cls.__name__,),
            )
            for task_cls in self.TASKS[self._settings.component]
        ]

    def _create_api_client(
        self, task_cls: type[BaseUpdaterTask]
    ) -> BaseCodexFFAPIClient:
        """Instantiate the HTTP client for a given updater task class."""
        return get_api_cls(settings=self._settings, updater_task_cls=task_cls)()
