import platform

import typer
from rich.panel import Panel

from ffmpeg_updater_win.app.banner import BANNER
from ffmpeg_updater_win.app.constants import (
    APP_NAME,
    APP_VERSION,
    WINDOWS_PLATFORM,
)
from ffmpeg_updater_win.app.enums import ExitCodeType
from ffmpeg_updater_win.app.utils import rich_console


def abort_on_non_windows() -> None:
    system: str = platform.system()
    if system != WINDOWS_PLATFORM:
        rich_console.print(BANNER)
        rich_console.print(
            Panel(
                f'[red]Unsupported system: {system}',
                title=f'{APP_NAME} {APP_VERSION}',
                border_style='red',
            )
        )
        raise typer.Exit(code=ExitCodeType.EXIT_ERROR)
