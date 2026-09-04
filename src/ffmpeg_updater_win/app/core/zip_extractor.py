"""Stream-extract required FFmpeg binaries from a zip download."""

import asyncio
from collections.abc import AsyncGenerator
from pathlib import Path

import aiofiles
from loguru import logger

from ffmpeg_updater_win.app.enums import RequiredFfbinaryType
from ffmpeg_updater_win.app.models.config import UpdaterConfig
from ffmpeg_updater_win.app.tasks.validation import FFmpegBinValidationTask
from ffmpeg_updater_win.app.utils import create_task


class ZipStreamExtractor:
    """Write FFmpeg executables from a zip member stream and validate them."""

    def __init__(self, settings: UpdaterConfig) -> None:
        """Bind extractor settings and prepare the validation-task list."""
        self._log = logger
        self._log.debug('Initializing "{}"', self.__class__.__name__)
        self._settings = settings
        self._validation_tasks = []

    async def process_zip_stream(
        self,
        stream_generator: AsyncGenerator[
            tuple[bytes, int, AsyncGenerator[bytes, None]], None
        ],
    ) -> None:
        """Extract required binaries from zip members and wait for validation."""
        ffbinaries = RequiredFfbinaryType.choices()
        written_files_count, ffbinaries_count = 0, len(ffbinaries)
        async for member_, _file_size, unzipped_chunks in stream_generator:
            member = member_.decode()
            filename = Path(member).name
            if filename not in ffbinaries:
                self._log.debug('Skip {}', member)
                async for _ in unzipped_chunks:
                    # Go through chunks for unneeded files and throw them out.
                    pass
                continue

            await self._write_file(filename, unzipped_chunks)
            written_files_count += 1
            if written_files_count == ffbinaries_count:
                break

        await asyncio.gather(*self._validation_tasks)
        self._log.info('All FFmpeg binaries updated, zip stream process done')

    async def _write_file(self, filename: str, unzipped_chunks) -> None:  # noqa: ANN001
        """Write unzipped chunks into the destination file."""
        file_path = self._settings.destination / filename
        self._log.debug('Write file {}', file_path)
        async with aiofiles.open(file_path, 'wb') as fd_out:
            async for chunk in unzipped_chunks:
                await fd_out.write(chunk)
        self._start_validation_task(file_path)

    def _start_validation_task(self, file_path: Path) -> None:
        """Spawn an executable validation task for a written binary."""
        self._validation_tasks.append(
            create_task(
                FFmpegBinValidationTask().validate(file_path),
                task_name=f'Validation<{file_path}>',
                log=self._log,
                exception_message='Task {} raised an exception',
                exception_message_args=(FFmpegBinValidationTask.__name__,),
            )
        )
