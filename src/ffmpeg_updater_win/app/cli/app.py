from pathlib import Path
from typing import Annotated, Final

import typer

from ffmpeg_updater_win.app.banner import BANNER
from ffmpeg_updater_win.app.cli.callbacks import version_callback
from ffmpeg_updater_win.app.cli.validators import abort_on_non_windows
from ffmpeg_updater_win.app.constants import DEFAULT_EXTRACT_PATH
from ffmpeg_updater_win.app.core.controller import MainAppController
from ffmpeg_updater_win.app.core.ffmpeg_updater import FFmpegUpdater
from ffmpeg_updater_win.app.enums import (
    CodexSourceType,
    FFSourceType,
    LogLevelType,
    UpdaterComponentType,
    WinPlatformType,
)
from ffmpeg_updater_win.app.log import init_logging
from ffmpeg_updater_win.app.models.config import UpdaterConfig
from ffmpeg_updater_win.app.utils import rich_console

typer_app: Final[typer.Typer] = typer.Typer(invoke_without_command=True)


@typer_app.callback()
def main(ctx: typer.Context) -> None:
    """FFmpeg updater CLI."""
    if ctx.invoked_subcommand is None:
        rich_console.print(BANNER)
        typer.echo(ctx.get_help())
        raise typer.Exit


@typer_app.command()
def run(  # noqa: PLR0913, PLR0917
    component: UpdaterComponentType = typer.Option(
        UpdaterComponentType.FFMPEG,
        '-c',
        '--component',
        help=f'FFmpeg Updater components to update; currently, '
        f'only "{UpdaterComponentType.FFMPEG}" is supported',
    ),
    destination: Path = typer.Option(
        DEFAULT_EXTRACT_PATH,
        '-d',
        '--destination',
        file_okay=False,
        dir_okay=True,
        help='FFmpeg destination directory path',
    ),
    platform: WinPlatformType = typer.Option(
        WinPlatformType.WIN64,
        '-p',
        '--platform',
        help='FFmpeg binaries os platform',
    ),
    force: bool = typer.Option(False, '-f', '--force', help='Perform force update'),  # noqa: FBT003
    ffmpeg_source: FFSourceType = typer.Option(
        FFSourceType.CODEX,
        '-fsrc',
        '--ffmpeg-source',
        help=f'FFmpeg binaries source; currently, only "{FFSourceType.CODEX}" is supported',
    ),
    codex_source: CodexSourceType = typer.Option(
        CodexSourceType.GITHUB,
        '-csrc',
        '--codex--source',
        help='Codex binaries download source',
    ),
    verbose: LogLevelType = typer.Option(
        LogLevelType.INFO, '-v', '--verbose', help='Log level 0-3'
    ),
    version: Annotated[  # noqa: ARG001
        bool | None,
        typer.Option(
            '-V', '--version', callback=version_callback, help='Show app version'
        ),
    ] = None,
) -> None:
    abort_on_non_windows()
    updater_config = UpdaterConfig(
        component=component,
        destination=destination,
        platform=platform,
        force=force,
        ffmpeg_source=ffmpeg_source,
        codex_source=codex_source,
        verbose=LogLevelType(verbose),
    )
    init_logging(log_level=updater_config.verbose)
    MainAppController(updater=FFmpegUpdater(config=updater_config)).run()
