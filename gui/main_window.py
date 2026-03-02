# -*- coding: utf-8 -*-
"""Main terminal window: banner, sections, progress, menu."""
import sys
try:
    from colorama import init, Fore, Style
    init(autoreset=True, convert=True)
    _HAS_COLOR = True
except ImportError:
    _HAS_COLOR = False
    Fore = Style = type("F", (), {"__getattr__": lambda s, n: ""})()

BOX_H = "\u2500"
BOX_V = "\u2502"
BOX_TL = "\u250c"
BOX_TR = "\u2510"
BOX_BL = "\u2514"
BOX_BR = "\u2518"
W = 62


def _c(text, color):
    return (color + text + Style.RESET_ALL) if _HAS_COLOR else text


# ASCII logo (from 2.txt) - SECURITY RESEARCH
LOGO_LINES = [
    " __          _______ _    _  _____    _____                      _ _          ",
    r" \ \        / / ____| |  | |/ ____|  / ____|                    (_) |         ",
    r"  \ \  /\  / / (___ | |  | | (___   | (___   ___  ___ _   _ _ __ _| |_ _   _  ",
    r"   \ \/  \/ / \___ \| |  | |\___ \   \___ \ / _ \/ __| | | | '__| | __| | | | ",
    r"    \  /\  /  ____) | |__| |____) |  ____) |  __/ (__| |_| | |  | | |_| |_| | ",
    r"     \/  \/  |_____/ \____/|_____/  |_____/ \___|\___|\__,_|_|  |_|\__|\__, | ",
    "                                                                        __/ | ",
    " _____                               _       _______          _ _    _|___/  ",
    r"|  __ \                             | |     |__   __|        | | |  (_) |    ",
    r"| |__) |___  ___  ___  __ _ _ __ ___| |__      | | ___   ___ | | | ___| |_   ",
    r"|  _  // _ \/ __|/ _ \/ _` | '__/ __| '_ \     | |/ _ \ / _ \| | |/ / | __|  ",
    r"| | \ \  __/\__ \  __/ (_| | | | (__| | | |    | | (_) | (_) | |   <| | |_   ",
    r"|_|  \_\___||___/\___|\__,_|_|  \___|_| |_|    |_|\___/ \___/|_|_|\_\_|\__|  ",
    "                                                                              ",
    "                                                                              ",
]


def banner():
    """Print application banner (ASCII logo)."""
    print()
    for ln in LOGO_LINES:
        print(_c(ln, Fore.CYAN))
    print()


def section(title):
    """Print section header box."""
    t = " " + title + " "
    fill = (W - 2 - len(t)) // 2
    left = BOX_H * max(0, fill)
    right = BOX_H * max(0, W - 2 - len(t) - fill)
    print()
    print(_c(BOX_TL + left + t + right + BOX_TR, Fore.YELLOW))
    print(_c(BOX_V + " " * (W - 2) + BOX_V, Fore.YELLOW))


def section_end():
    print(_c(BOX_BL + BOX_H * (W - 2) + BOX_BR, Fore.YELLOW))


def line(text):
    s = (" " + str(text))[: W - 4].ljust(W - 4)
    print(_c(BOX_V + s + BOX_V, Fore.YELLOW))


def ok(msg):
    print(_c("[+] ", Fore.GREEN) + msg)


def fail(msg):
    print(_c("[-] ", Fore.RED) + msg)


def warn(msg):
    print(_c("[!] ", Fore.YELLOW) + msg)


def info(msg):
    print(_c("[*] ", Fore.CYAN) + msg)


def progress(current, total, prefix="Frame"):
    """Simple progress line."""
    pct = (100 * current / total) if total else 0
    bar_len = 24
    filled = int(bar_len * current / total) if total else 0
    bar = "\u2588" * filled + "\u2591" * (bar_len - filled)
    print(_c(f"  {prefix} ", Fore.CYAN) + bar + _c(f" {current}/{total} ({pct:.0f}%)", Fore.LIGHTBLACK_EX), end="\r")
    if current >= total:
        print()


def menu():
    """Print command menu."""
    section(" Commands ")
    line("  run <video_path>     Process video (detect + inpainting)")
    line("  validate <path>      Validate input file")
    line("  gpu                  Show GPU status")
    line("  install / 1          Install dependencies")
    line("  about               About (README)")
    line("  settings            Settings (device, output_dir, log_level)")
    line("  help                Show this menu")
    line("  quit / exit         Exit")
    line("")
    section_end()


def launcher_screen():
    """Print start screen: [1] Install, [2] Start, [3] About, [4] Settings."""
    print()
    print(_c(BOX_TL + BOX_H * (W - 2) + BOX_TR, Fore.CYAN))
    print(_c(BOX_V + "  [1] Install dependencies                         ".ljust(W - 2) + BOX_V, Fore.CYAN))
    print(_c(BOX_V + "  [2] Start                                        ".ljust(W - 2) + BOX_V, Fore.CYAN))
    print(_c(BOX_V + "  [3] About                                        ".ljust(W - 2) + BOX_V, Fore.CYAN))
    print(_c(BOX_V + "  [4] Settings                                     ".ljust(W - 2) + BOX_V, Fore.CYAN))
    print(_c(BOX_BL + BOX_H * (W - 2) + BOX_BR, Fore.CYAN))
    print()


class MainWindow:
    """CMD console main window: runs the interactive loop or single command."""

    def __init__(self):
        self.running = True

    def show_banner(self):
        banner()

    def show_menu(self):
        menu()

    def run_interactive(self):
        """Simple interactive loop."""
        self.show_banner()
        self.show_menu()
        info("Enter command (or 'quit' to exit).")
        while self.running:
            try:
                raw = input(_c("\n> ", Fore.GREEN)).strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not raw:
                continue
            parts = raw.split(maxsplit=1)
            cmd = (parts[0] or "").lower()
            arg = (parts[1] or "").strip() if len(parts) > 1 else ""
            if cmd in ("quit", "exit", "q"):
                ok("Goodbye.")
                break
            if cmd == "help":
                self.show_menu()
                continue
            yield cmd, arg
