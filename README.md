## FFmpeg binaries updater for Windows

Updates FFmpeg binaries (`ffmpeg.exe`, `ffplay.exe` and `ffprobe.exe`) from 
Codex FFmpeg builds (https://www.gyan.dev/ffmpeg/builds) with their latest versions.

## Requirements

Python 3.12+

## Installation

```text
uv tool install git+https://github.com/tropicoo/youtube-dl-ffmpeg-updater-win
```

## Usage

```text
> ffmpeg-updater-win run --force --platform win64 --verbose 3

2026-08-03 01:32:08.443 | INFO     | main           run                     :  90 | 


███████╗███████╗███╗   ███╗██████╗ ███████╗ ██████╗     ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██████╗
██╔════╝██╔════╝████╗ ████║██╔══██╗██╔════╝██╔════╝     ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
█████╗  █████╗  ██╔████╔██║██████╔╝█████╗  ██║  ███╗    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██████╔╝
██╔══╝  ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██╔══╝  ██║   ██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ██╔══██╗
██║     ██║     ██║ ╚═╝ ██║██║     ███████╗╚██████╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗██║  ██║
╚═╝     ╚═╝     ╚═╝     ╚═╝╚═╝     ╚══════╝ ╚═════╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝


2026-08-03 01:32:08.443 | INFO     | main           run                     :  91 | Starting main app
2026-08-03 01:32:08.444 | INFO     | updater        __init__                :  18 | Initializing "Updater" version 0.4.11
2026-08-03 01:32:08.444 | DEBUG    | managers       __init__                :  26 | Initializing "TaskManager"
2026-08-03 01:32:08.445 | INFO     | updater        run                     :  26 | Starting force update
2026-08-03 01:32:08.445 | DEBUG    | abstract       __init__                :  13 | Initializing "CodexFFGithubApiClient"
2026-08-03 01:32:08.446 | DEBUG    | abstract       __init__                :  19 | Initializing "CodexFfmpegUpdaterTask"
2026-08-03 01:32:08.446 | DEBUG    | zip_extractor  __init__                :  21 | Initializing "ZipStreamExtractor"
2026-08-03 01:32:08.446 | INFO     | abstract       _update                 :  46 | Updating FFmpeg binaries from codex
2026-08-03 01:32:08.446 | DEBUG    | client         _get_latest_tag         : 121 | GET https://github.com/GyanD/codexffmpeg/releases/latest
2026-08-03 01:32:09.195 | INFO     | client         download_latest_version :  25 | Latest version: "8.1.2"
2026-08-03 01:32:09.196 | DEBUG    | client         zipped_chunks_generator :  37 | GET https://github.com/GyanD/codexffmpeg/releases/download/8.1.2/ffmpeg-8.1.2-essentials_build.zip
2026-08-03 01:32:09.196 | DEBUG    | client         zipped_chunks_generator :  38 | Start download ffmpeg-8.1.2-essentials_build.zip
2026-08-03 01:32:09.572 | DEBUG    | zip_extractor  process_zip_stream      :  38 | Skip ffmpeg-8.1.2-essentials_build/
2026-08-03 01:32:09.572 | DEBUG    | zip_extractor  process_zip_stream      :  38 | Skip ffmpeg-8.1.2-essentials_build/bin/
2026-08-03 01:32:09.573 | DEBUG    | zip_extractor  _write_file             :  55 | Write file C:\youtube-dl\ffmpeg.exe
2026-08-03 01:32:10.887 | DEBUG    | zip_extractor  _write_file             :  55 | Write file C:\youtube-dl\ffplay.exe
2026-08-03 01:32:12.458 | DEBUG    | utils          get_stdout              :  68 | Command "('C:/youtube-dl/ffmpeg.exe', '-version')" exited with returncode 0
2026-08-03 01:32:12.459 | INFO     | validation     validate                :  16 | C:\youtube-dl\ffmpeg.exe successfully validated
2026-08-03 01:32:14.291 | DEBUG    | zip_extractor  _write_file             :  55 | Write file C:\youtube-dl\ffprobe.exe
2026-08-03 01:32:15.328 | DEBUG    | utils          get_stdout              :  68 | Command "('C:/youtube-dl/ffplay.exe', '-version')" exited with returncode 0
2026-08-03 01:32:15.329 | INFO     | validation     validate                :  16 | C:\youtube-dl\ffplay.exe successfully validated
2026-08-03 01:32:17.549 | DEBUG    | utils          get_stdout              :  68 | Command "('C:/youtube-dl/ffprobe.exe', '-version')" exited with returncode 0
2026-08-03 01:32:17.549 | INFO     | validation     validate                :  16 | C:\youtube-dl\ffprobe.exe successfully validated
2026-08-03 01:32:17.549 | INFO     | zip_extractor  process_zip_stream      :  50 | All ffbinaries updated, zip stream process done
2026-08-03 01:32:17.549 | DEBUG    | abstract       close_session           :  26 | Close client session
2026-08-03 01:32:17.551 | INFO     | updater        run                     :  29 | Force update finished
2026-08-03 01:32:17.552 | INFO     | main           run                     :  95 | Exiting main app
```

## Help

```text
> ffmpeg-updater-win run --help
                                                                                                                                         
 Usage: ffmpeg-updater-win run [OPTIONS]                                                                                                 
                                                                                                                                         
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --component      -c         <ffmpeg>        Updater components to update; currently, only "ffmpeg" is supported [default: ffmpeg]     │
│ --destination    -d         <directory>     Ffmpeg destination directory path [default: C:\youtube-dl]                                │
│ --platform       -p         <win32|win64>   Ffmpeg binaries os platform [default: win64]                                              │
│ --force          -f                         Perform force update                                                                      │
│ --ffmpeg-source  -fsrc      <codex>         Ffmpeg binaries source; currently, only "codex" is supported [default: codex]             │
│ --codex-source   -csrc      <github|codex>  Codex binaries download source [default: github]                                          │
│ --verbose        -v         <0|1|2|3>       Log level 0-3 [default: 2]                                                                │
│ --version        -V                         Show app version                                                                          │
│ --help                                      Show this message and exit.                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Misc

Easily run as batch file `ffmpeg-updater-win.bat` on Windows.

```text
:: "ffmpeg-updater-win.bat" file content

@echo off
ffmpeg-updater-win run --platform win64 --verbose 3

pause
```
