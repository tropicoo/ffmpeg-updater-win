"""Post-extract checks that written FFmpeg binaries can run."""

from pathlib import Path

from loguru import logger

from ffmpeg_updater_win.app.utils import get_stdout


class FFmpegBinValidationTask:
    """Run `-version` on an extracted FFmpeg executable."""

    def __init__(self) -> None:
        """Bind the shared logger."""
        self._log = logger

    async def validate(self, bin_path: Path) -> None:
        """Execute the binary with `-version` and fail on stderr output."""
        _ = await get_stdout(
            cmd=(bin_path.as_posix(), '-version'), log=self._log, raise_on_stderr=True
        )
        self._log.info('{} successfully validated', bin_path)
