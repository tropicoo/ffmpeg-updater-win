"""Managers Module."""

from asyncio import Task
from typing import ClassVar

from loguru import logger

from ffmpeg_updater_win.app.clients.codex.abstract import BaseCodexFFAPIClient
from ffmpeg_updater_win.app.clients.codex.mappings import get_api_cls
from ffmpeg_updater_win.app.enums import UpdaterComponentType
from ffmpeg_updater_win.app.models.config import UpdaterConfig
from ffmpeg_updater_win.app.tasks.abstract import BaseUpdaterTask
from ffmpeg_updater_win.app.tasks.codex import CodexFfmpegUpdaterTask
from ffmpeg_updater_win.app.utils import create_task


class TaskManager:
    TASKS: ClassVar[dict[UpdaterComponentType, tuple[type[BaseUpdaterTask], ...]]] = {
        UpdaterComponentType.FFMPEG: (CodexFfmpegUpdaterTask,),
    }

    def __init__(self, settings: UpdaterConfig) -> None:
        self._log = logger
        self._log.debug('Initializing "{}"', self.__class__.__name__)
        self._settings = settings

    def create_tasks(self) -> list[Task]:
        tasks: list[Task] = []
        for task_cls in self.TASKS[self._settings.component]:
            tasks.append(
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
            )
        return tasks

    def _create_api_client(
        self, task_cls: type[BaseUpdaterTask]
    ) -> BaseCodexFFAPIClient:
        return get_api_cls(settings=self._settings, updater_task_cls=task_cls)()
