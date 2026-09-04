"""Application exception hierarchy."""


class BaseUpdaterError(Exception):
    """Base exception for all updater errors."""


class FFmpegUpdaterError(BaseUpdaterError):
    """Error raised by FFmpeg update orchestration."""


class NoFileToExtractError(FFmpegUpdaterError):
    """Raised when the archive does not contain required FFmpeg binaries."""


class CommandError(FFmpegUpdaterError):
    """Raised when a subprocess fails, times out, or writes unexpected stderr."""
