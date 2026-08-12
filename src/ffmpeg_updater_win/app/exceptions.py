"""Exceptions Module."""


class BaseUpdaterError(Exception):
    pass


class FFmpegUpdaterError(BaseUpdaterError):
    """FFmpeg Updater Base Exception Class."""


class NoFileToExtractError(FFmpegUpdaterError):
    pass


class CommandError(FFmpegUpdaterError):
    pass
