"""Enumerations used by the CLI, config, and Codex clients."""

from enum import IntEnum, StrEnum


class BaseStrChoiceEnum(StrEnum):
    """String enum that can expose its values as a choice set."""

    @classmethod
    def choices(cls) -> frozenset[str]:
        """Return the set of enum values for membership checks and CLI choices."""
        return frozenset(member.value for member in cls)


class LogLevelType(IntEnum):
    """Numeric `--verbose` values mapped to Loguru level names."""

    ERROR = 0
    """Only error messages."""

    WARNING = 1
    """Warnings and errors."""

    INFO = 2
    """Informational messages (default)."""

    DEBUG = 3
    """Debug messages including HTTP and subprocess details."""


class ExitCodeType(IntEnum):
    """Process exit codes returned by the CLI."""

    EXIT_OK = 0
    """Successful run."""

    EXIT_ERROR = 1
    """Fatal error (unsupported OS, failed update, or other unrecoverable error)."""


class UpdaterComponentType(BaseStrChoiceEnum):
    """Updatable components exposed by `--component`."""

    FFMPEG = 'ffmpeg'
    """FFmpeg binaries (`ffmpeg`, `ffprobe`, `ffplay`)."""


class WinPlatformType(BaseStrChoiceEnum):
    """Windows architectures accepted by `--platform`."""

    WIN32 = 'win32'
    """32-bit Windows (Codex builds are 64-bit only)."""

    WIN64 = 'win64'
    """64-bit Windows."""


class FFSourceType(BaseStrChoiceEnum):
    """FFmpeg binary providers accepted by `--ffmpeg-source`."""

    CODEX = 'codex'
    """Gyan/Codex FFmpeg builds."""


class CodexReleaseType(BaseStrChoiceEnum):
    """Codex release channels used in archive names and version URLs."""

    GIT = 'git'
    """Latest git master build."""

    RELEASE = 'release'
    """Latest numbered release build."""

    TOOLS = 'tools'
    """Standalone tools build."""


class CodexBuildType(BaseStrChoiceEnum):
    """Codex archive flavors (essentials vs full)."""

    ESSENTIALS = 'essentials'
    """Smaller essentials build containing the three main binaries."""

    FULL = 'full'
    """Full build with extra libraries and filters."""


class RequiredFfbinaryType(BaseStrChoiceEnum):
    """Windows executables that must be present after an update."""

    FFMPEG = 'ffmpeg.exe'
    """Main FFmpeg encoder/decoder CLI."""

    FFPROBE = 'ffprobe.exe'
    """Media probe CLI."""

    FFPLAY = 'ffplay.exe'
    """Simple media player CLI."""


class CodexSourceType(BaseStrChoiceEnum):
    """Where Codex zip archives are downloaded from."""

    GITHUB = 'github'
    """GitHub Releases of `GyanD/codexffmpeg`."""

    CODEX = 'codex'
    """Direct downloads from gyan.dev."""


class CodexAPIPathType(BaseStrChoiceEnum):
    """Relative paths under the gyan.dev FFmpeg builds root."""

    CHANGELOG_COUNTER = 'changelog-counter'
    """Changelog revision counter endpoint."""

    LATEST_GIT_VER = 'git-version'
    """Plain-text latest git build version."""

    LATEST_RELEASE_VER = 'release-version'
    """Plain-text latest release version."""

    LATEST_TOOLS_VER = 'tools-version'
    """Plain-text latest tools version."""

    LAST_BUILD_UPDATE = 'last-build-update'
    """Timestamp of the last published build."""

    NEXT_BUILD_UPDATE = 'next-build-update'
    """Timestamp of the next expected build."""


class CodexArchExtensionType(BaseStrChoiceEnum):
    """Archive extensions used in Codex download filenames."""

    ZIP = 'zip'
    """ZIP archive (streamed by this updater)."""

    SEVEN_ZIP = '7z'
    """7-Zip archive (not used for streaming)."""
