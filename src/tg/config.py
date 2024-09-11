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


#region Paths
CONFIG_DIR = Path(os.getenv("XDG_CONFIG_HOME", "~/.config") + "/tg/").expanduser()
FILES_DIR = Path(os.getenv("XDG_CACHE_HOME", "~/.cache") + "/tg/").expanduser()
DOWNLOAD_DIR = Path(os.getenv("XDG_DOWNLOAD_DIR", "~/Downloads")).expanduser()
LOG_DIR = Path(os.getenv("XDG_DATA_HOME", "~/.local/share") + "/tg/").expanduser()

CONFIG_FILE = CONFIG_DIR / "conf.py"
LOGGING_CONFIG = CONFIG_DIR / "logging.conf"

ICON_PATH = str(Path(__file__).parent / "resources" / "tg.png")

TDLIB_PATH = None

MAILCAP_FILE: Optional[str] = None
#endregion

LOG_LEVEL = 'INFO'

API_ID = "559815"
API_HASH = "fd121358f59d764c57c55871aa0807ca"

PHONE = None
ENC_KEY = ""

TDLIB_VERBOSITY = 0

MAX_DOWNLOAD_SIZE = "10MB"

# region Commands
FILE_PICKER_CMD = "ranger --choosefile={file_path}"

if _os_name == _darwin:
    NOTIFY_CMD = "terminal-notifier -group chat-{chat_id}"\
        "-title {title} -subtitle {subtitle} -message {msg} -appIcon {icon_path}"
else:
    # notify-send doesn't notification grouping implementation isn't very useful
    NOTIFY_CMD = "notify-send --category=im.received '\
        '--app-name={title} --icon={icon_path} {subtitle} {msg}"
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

DEFAULT_OPEN = ('xdg-' if _os_name == _linux else '') + "open {file_path}"

if _os_name == _linux:
    COPY_CMD = "wl-copy" if os.environ.get("WAYLAND_DISPLAY") else "xclip -selection c"
else:
    COPY_CMD = "pbcopy"

URL_VIEW = "urlview"
#endregion

#region String constants
CHAT_FLAGS: dict[str, str] = {}

MSG_FLAGS: dict[str, str] = {}

REPLY_MSG_PREFIX = "# >"
#endregion

#region Colors
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
#endregion

KEEP_MEDIA = 7

NOTIFY_TYPING = True

TIMESTAMP_FORMAT = {
    'chat': '%d %H:%M:%S',
    'navigation': '  %H:%M:%S',
    'navigation_old': '%Y-%m-%d',
}

# delay in milliseconds before message list render
# used to delay message list update on chat selection
MESSAGES_RENDER_DELAY = 250

# start scrolling to next page when number of the msgs left is less than value.
# note, that setting high values could lead to situations when long msgs will
# be removed from the display in order to achive scroll threshold. this could
# cause blan areas on the msg display screen
MSGS_LEFT_SCROLL_THRESHOLD = 2

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
