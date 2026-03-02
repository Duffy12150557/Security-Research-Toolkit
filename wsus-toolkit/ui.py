# -*- coding: utf-8 -*-
"""Terminal UI for WSUS Security Research Toolkit."""
import sys
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True, convert=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    Fore = Back = Style = type('F', (), {'__getattr__': lambda s, n: ''})()

# Box-drawing (CP437/UTF-8)
BOX_H = '\u2500'
BOX_V = '\u2502'
BOX_TL = '\u250c'
BOX_TR = '\u2510'
BOX_BL = '\u2514'
BOX_BR = '\u2518'
BOX_CROSS = '\u253c'


def _color(text, color):
    return (color + text + Style.RESET_ALL) if HAS_COLOR else text


def banner():
    """Print toolkit banner."""
    lines = [
        '',
        BOX_TL + BOX_H * 58 + BOX_TR,
        BOX_V + '  WSUS Security Research Toolkit  [CVE-2025-59287]  '.ljust(58) + BOX_V,
        BOX_V + '  Authorized Security Testing Only                    '.ljust(58) + BOX_V,
        BOX_BL + BOX_H * 58 + BOX_BR,
        ''
    ]
    print(_color('\n'.join(lines), Fore.CYAN))


def box(title, width=60):
    """Return top border of a box with title."""
    fill = (width - 4 - len(title)) // 2
    left = BOX_H * max(0, fill)
    right = BOX_H * max(0, width - 4 - len(title) - fill)
    return _color(BOX_TL + left + ' ' + title + ' ' + right + BOX_TR, Fore.YELLOW)


def box_bottom(width=60):
    """Return bottom border of a box."""
    return _color(BOX_BL + BOX_H * (width - 2) + BOX_BR, Fore.YELLOW)


def line(text, width=60):
    """Return a box line with text."""
    padded = (' ' + str(text))[:width - 4].ljust(width - 4)
    return _color(BOX_V + padded + BOX_V, Fore.YELLOW)


def ok(msg):
    print(_color('[+] ', Fore.GREEN) + msg)


def fail(msg):
    print(_color('[-] ', Fore.RED) + msg)


def warn(msg):
    print(_color('[!] ', Fore.YELLOW) + msg)


def info(msg):
    print(_color('[*] ', Fore.CYAN) + msg)


def section(title):
    print()
    print(box(title))
    print(line(''))


def separator():
    print(_color('  ' + BOX_H * 56 + '  ', Fore.DIM))


def usage_help():
    """Print formatted help."""
    banner()
    print(box(' Usage ', 60))
    print(line('  python exp.py <TARGET_URL> [OPTIONS]', 60))
    print(line('', 60))
    print(line('  TARGET_URL   WSUS server URL (e.g. http://192.168.1.100:8533)', 60))
    print(line('', 60))
    print(line('  OPTIONS:', 60))
    print(line('    --no-wait    Skip delay between requests', 60))
    print(line('    --help       Show this help', 60))
    print(line('', 60))
    print(box_bottom(60))
    print()
    print(box(' Examples ', 60))
    print(line('  python exp.py http://192.168.1.100:8533', 60))
    print(line('  python exp.py http://wsus-lab.local:8534 --no-wait', 60))
    print(box_bottom(60))
    print()
