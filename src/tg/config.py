"""
Every parameter (except for CONFIG_FILE) can be
overwritten by external config file
"""

import os
import platform
import runpy
from pathlib import Path
from typing import Optional

import tg.colors

_os_name = platform.system()
_darwin = "Darwin"
_linux = "Linux"


CONFIG_HOME = os.getenv("XDG_CONFIG_HOME", "~/.config")
CACHE_HOME = os.getenv("XDG_CACHE_HOME", "~/.cache")
DATA_HOME = os.getenv("XDG_DATA_HOME", "~/.local/share")
DOWNLOAD_HOME = os.getenv("XDG_DOWNLOAD_DIR", "~/Downloads")

CONFIG_DIR = Path(CONFIG_HOME + "/tg/").expanduser()
CONFIG_FILE = CONFIG_DIR / "conf.py"
FILES_DIR = Path(CACHE_HOME + "/tg/").expanduser()
DOWNLOAD_DIR = Path(DOWNLOAD_HOME).expanduser()

MAILCAP_FILE: Optional[str] = None

LOG_LEVEL = "INFO"
LOG_PATH = Path("~/.local/share/tg/").expanduser()

API_ID = "559815"
API_HASH = "fd121358f59d764c57c55871aa0807ca"

PHONE = None
ENC_KEY = ""

TDLIB_PATH = None
TDLIB_VERBOSITY = 0

MAX_DOWNLOAD_SIZE = "10MB"

FILE_PICKER_CMD = "ranger --choosefile={file_path}"

if _os_name == _darwin:
    NOTIFY_CMD = "terminal-notifier "\
        "-title {title} -subtitle {subtitle} -message {msg} -appIcon {icon_path}"
else:
    NOTIFY_CMD = "notify-send "
NOTIFY_TYPES = { 'private', 'group' }

VIEW_TEXT_CMD = "less"
FZF = "fzf"

if _os_name == _linux:
    # for more info see https://trac.ffmpeg.org/wiki/Capture/ALSA
    VOICE_RECORD_CMD = "ffmpeg -y -f alsa -i hw:0 -c:a libopus -b:a 32k {file_path}"
else:
    VOICE_RECORD_CMD = "ffmpeg -y -f avfoundation -i ':0' -c:a libopus -b:a 32k {file_path}"

LONG_MSG_CMD = "vim + -c 'startinsert' {file_path}"
EDITOR = os.environ.get("EDITOR", "vi")

DEFAULT_OPEN = "xdg-open" if _os_name == _linux else "open"

if _os_name == _linux:
    COPY_CMD = "wl-copy" if os.environ.get("WAYLAND_DISPLAY") else "xclip -selection c"
else:
    COPY_CMD = "pbcopy"

CHAT_FLAGS: dict[str, str] = {}

MSG_FLAGS: dict[str, str] = {}

ICON_PATH = str(Path(__file__).parent / "resources" / "tg.png")

URL_VIEW = "urlview"

USERS_COLORS = list(range(20, 231))
for i in 22,52:
    USERS_COLORS.remove(i)

COLOR_TITLE = tg.colors.cyan
COLOR_TIME = tg.colors.cyan
COLOR_FLAGS = tg.colors.yellow
COLOR_UNREAD_COUNT = tg.colors.yellow
COLOR_MSG_MINE = tg.colors.white
BGCOLOR_MSG_MINE = tg.colors.black
COLOR_MSG_MEDIA = tg.colors.magenta
COLOR_MSG_URL = tg.colors.blue
COLOR_MSG_REPLY = tg.colors.cyan
COLOR_MSG_NORMAL = -1

#preview of last message in chat window
COLOR_MSG_LAST = -1

KEEP_MEDIA = 7

NOTIFY_TYPING = True

TIMESTAMP_FORMAT = {
    'chat': '%d %H:%M:%S',
    'navigation': '  %H:%M:%S',
    'navigation_old': '%Y-%m-%d',
}

if CONFIG_FILE.is_file():
    config_params = runpy.run_path(CONFIG_FILE)  # type: ignore
    for param, value in config_params.items():
        if param.isupper():
            globals()[param] = value
else:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not PHONE:
        print("Enter your phone number in international format (including country code)")
        PHONE = input("phone> ")
        if not PHONE.startswith("+"):
            PHONE = "+" + PHONE

    with open(CONFIG_FILE, "w") as f:
        f.write(f"PHONE = '{PHONE}'\n")
