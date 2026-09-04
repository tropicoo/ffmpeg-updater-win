"""Console-script entrypoint for the FFmpeg updater CLI."""

from ffmpeg_updater_win.app.cli.app import typer_app


def main() -> None:
    """Run the Typer application."""
    typer_app()
