"""
Every parameter (except for CONFIG_FILE) can be
overwritten by external config file
"""
import os
import platform
import runpy
import tg.colors
from typing import Dict, Optional

_os_name = platform.system()
_darwin = "Darwin"
_linux = "Linux"

def expand_path(path):
    return os.path.expandvars(os.path.expanduser(path))

CONFIG_HOME = expand_path(os.getenv("XDG_CONFIG_HOME", "~/.config"))
CACHE_HOME = expand_path(os.getenv("XDG_CACHE_HOME", "~/.cache"))
DATA_HOME = expand_path(os.getenv("XD_GDATA_HOME", "~/.local/share"))
DOWNLOAD_DIR = expand_path(os.getenv("XDG_DOWNLOAD_DIR", "~/Downloads"))

CONFIG_DIR = os.path.join(CONFIG_HOME, "tg/")
CONFIG_FILE = os.path.join(CONFIG_DIR, "conf.py")
FILES_DIR = os.path.join(CACHE_HOME, "tg/")

LOG_LEVEL = "INFO"
LOG_PATH = expand_path(DATA_HOME + "/tg/")

API_ID = "559815"
API_HASH = "fd121358f59d764c57c55871aa0807ca"

PHONE = None
ENC_KEY = ""

TDLIB_PATH = None
TDLIB_VERBOSITY = 0

MAX_DOWNLOAD_SIZE = "10MB"

# TODO: check platform
NOTIFY_CMD = "/usr/local/bin/terminal-notifier -title {title} -subtitle {subtitle} -message {msg} -appIcon {icon_path}"
NOTIFY_TYPES = { 'private', 'group' }

VIEW_TEXT_CMD = "less"
FZF = "fzf"

if _os_name == _linux:
    # for more info see https://trac.ffmpeg.org/wiki/Capture/ALSA
    VOICE_RECORD_CMD = (
        "ffmpeg -f alsa -i hw:0 -c:a libopus -b:a 32k {file_path}"
    )
else:
    VOICE_RECORD_CMD = (
        "ffmpeg -f avfoundation -i ':0' -c:a libopus -b:a 32k {file_path}"
    )

LONG_MSG_CMD = "vim + -c 'startinsert' {file_path}"
EDITOR = os.environ.get("EDITOR", "vi")

if _os_name == _linux:
    DEFAULT_OPEN = "xdg-open"
else:
    DEFAULT_OPEN = "open"

if _os_name == _linux:
    if os.environ.get("WAYLAND_DISPLAY"):
        COPY_CMD = "wl-copy"
    else:
        COPY_CMD = "xclip -selection c"
else:
    COPY_CMD = "pbcopy"

CHAT_FLAGS: Dict[str, str] = {}

MSG_FLAGS: Dict[str, str] = {}

ICON_PATH = os.path.join(os.path.dirname(__file__), "resources", "tg.png")

URL_VIEW = "urlview"

USERS_COLORS = list(range(20, 231))
for i in 22,52: USERS_COLORS.remove(i)

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

FILE_PICKER_CMD = "ranger --choosefile={file_path}"

DOWNLOAD_DIR = expand_path("$XDG_DOWNLOAD_DIR")

TIMESTAMP_FORMAT = {
    'chat': '%d %H:%M:%S',
    'navigation': '  %H:%M:%S',
    'navigation_old': '%Y-%m-%d',
}

if os.path.isfile(CONFIG_FILE):
    config_params = runpy.run_path(CONFIG_FILE)  # type: ignore
    for param, value in config_params.items():
        if param.isupper():
            globals()[param] = value
else:
    os.makedirs(CONFIG_DIR, exist_ok=True)

    if not PHONE:
        print(
            "Enter your phone number in international format (including country code)"
        )
        PHONE = input("phone> ")
        if not PHONE.startswith("+"):
            PHONE = "+" + PHONE

    with open(CONFIG_FILE, "w") as f:
        f.write(f"PHONE = '{PHONE}'\n")
