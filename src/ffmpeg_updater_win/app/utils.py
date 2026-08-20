"""Utils Module."""

import asyncio
import functools
from collections.abc import Coroutine
from io import StringIO
from typing import TYPE_CHECKING, Any, Final

from loguru import logger
from rich.console import Console

from ffmpeg_updater_win.app.exceptions import CommandError

if TYPE_CHECKING:
    from loguru import Logger  # noqa: TC004

rich_console: Final[Console] = Console()

_DEFAULT_COMMAND_TIMEOUT: Final[int] = 10


async def get_stdout(
    cmd: list[str] | tuple[str, ...],
    log: Logger | None = None,
    raise_on_stderr: bool = False,
    timeout: float = _DEFAULT_COMMAND_TIMEOUT,
) -> str:
    log = log or logger
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout)
    except TimeoutError as err:
        proc.kill()
        await proc.wait()
        log.error('Command "{}" timed out after {} seconds', cmd, timeout)  # noqa: TRY400
        raise CommandError(f'Command timed out: {cmd}') from err

    log.debug('Command "{}" exited with returncode {}', cmd, proc.returncode)

    stdout_decoded = stdout.decode(errors='replace')
    stderr_decoded = stderr.decode(errors='replace')

    if stderr_decoded:
        log.warning('[stderr] {}', stderr_decoded)
        if raise_on_stderr:
            raise CommandError(stderr_decoded)
    return stdout_decoded


def create_task[T](  # noqa: PLR0913
    coroutine: Coroutine[Any, Any, T],
    *,
    log: Logger,
    task_name: str | None = None,
    exception_message: str = 'Task raised an exception',
    exception_message_args: tuple[Any, ...] = (),
    loop: asyncio.AbstractEventLoop | None = None,
) -> asyncio.Task[T]:
    if loop is None:
        loop = asyncio.get_running_loop()
    task = loop.create_task(coroutine, name=task_name)
    task.add_done_callback(
        functools.partial(
            _handle_task_result,
            log=log,
            exception_message=exception_message,
            exception_message_args=exception_message_args,
        )
    )
    return task


def _handle_task_result(
    task: asyncio.Task,
    *,
    log: Logger,
    exception_message: str,
    exception_message_args: tuple[Any, ...] = (),
) -> None:
    try:
        task.result()
    except asyncio.CancelledError:
        pass
    except Exception:
        log.exception(exception_message, *exception_message_args)


def render_to_ansi(renderable: Any, *, width: int | None = None) -> str:
    buf = StringIO()
    console = Console(file=buf, width=width)
    console.print(renderable)
    return buf.getvalue()
