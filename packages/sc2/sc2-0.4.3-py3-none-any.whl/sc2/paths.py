import os
from pathlib import Path
import platform

import logging
logger = logging.getLogger(__name__)

BASEDIR = {
    "Windows": "C:/Program Files (x86)/StarCraft II",
    "Darwin": "/Applications/StarCraft II",
    "Linux": "~/StarCraftII"
}

BINPATH = {
    "Windows": "SC2_x64.exe",
    "Darwin": "SC2.app/Contents/MacOS/SC2",
    "Linux": "SC2_x64"
}

CWD = {
    "Windows": "Support64",
    "Darwin": None,
    "Linux": None
}

PF = platform.system()

if PF not in BASEDIR:
    logger.critical(f"Unsupported platform '{PF}'")
    exit(1)

def get_env():
    # TODO: Linux env conf from: https://github.com/deepmind/pysc2/blob/master/pysc2/run_configs/platforms.py
    return None

def latest_executeble(versions_dir):
    latest = max((int(p.name[4:]), p) for p in versions_dir.iterdir() if p.is_dir() and p.name.startswith("Base"))
    version, path = latest
    if version < 55958:
        logger.critical(f"Your SC2 binary is too old. Upgrade to 3.16.1 or newer.")
        exit(1)
    return path / BINPATH[PF]

class Paths(object):
    try:
        BASE = Path(os.environ.get("SC2PATH", BASEDIR[PF])).expanduser()
        EXECUTABLE = latest_executeble(BASE / "Versions")
        CWD = base_dir / CWD[PF] if CWD[PF] else None

        REPLAYS = BASE / "Replays"
        MAPS = BASE / "Maps"
    except FileNotFoundError as e:
        logger.critical(f"SC2 installation not found: File '{e.filename}' does not exist.")
        exit(1)
