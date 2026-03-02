# -*- coding: utf-8 -*-
"""Application logging with styled terminal output."""
import sys
from datetime import datetime

try:
    from colorama import init, Fore, Style
    init(autoreset=True, convert=True)
    _HAS_COLOR = True
except ImportError:
    _HAS_COLOR = False
    Fore = Style = type("F", (), {"__getattr__": lambda s, n: ""})()


def _color(text, color):
    return (color + text + Style.RESET_ALL) if _HAS_COLOR else text


def _ts():
    return datetime.now().strftime("%H:%M:%S")


def debug(msg):
    print(_color(f"[{_ts()}] ", Fore.BLACK) + _color("DBG ", Fore.LIGHTBLACK_EX) + str(msg))


def info(msg):
    print(_color(f"[{_ts()}] ", Fore.BLACK) + _color("INF ", Fore.CYAN) + str(msg))


def warning(msg):
    print(_color(f"[{_ts()}] ", Fore.BLACK) + _color("WRN ", Fore.YELLOW) + str(msg))


def error(msg):
    print(_color(f"[{_ts()}] ", Fore.BLACK) + _color("ERR ", Fore.RED) + str(msg), file=sys.stderr)


def success(msg):
    print(_color(f"[{_ts()}] ", Fore.BLACK) + _color("OK  ", Fore.GREEN) + str(msg))
