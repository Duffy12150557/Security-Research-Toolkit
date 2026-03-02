# -*- coding: utf-8 -*-
"""Application entry point. Interactive terminal interface."""
import argparse
import importlib
import subprocess
import sys
import os

# Ensure project root is on path
_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ROOT)

_REQUIREMENTS = os.path.join(_ROOT, "requirements.txt")
_DEPS = ["colorama"]  # required package names to check


def check_dependencies():
    """Return (all_ok: bool, missing: list of str)."""
    missing = []
    for name in _DEPS:
        try:
            __import__(name)
        except ImportError:
            missing.append(name)
    return (len(missing) == 0, missing)


def install_dependencies():
    """Run pip install -r requirements.txt. Return True on success."""
    if not os.path.isfile(_REQUIREMENTS):
        return False
    try:
        code = subprocess.call(
            [sys.executable, "-m", "pip", "install", "-r", _REQUIREMENTS],
            cwd=_ROOT,
        )
        return code == 0
    except Exception:
        return False


from gui.main_window import (
    MainWindow,
    banner,
    section,
    section_end,
    line,
    ok,
    fail,
    warn,
    info,
    progress,
    launcher_screen,
)
from core.validator import validate_input_path
from core.processor import process_video, process_image
from utils import ensure_env
from utils.gpu_manager import get_gpu_info, suggest_device
from utils.settings import load as load_settings, save as save_settings, DEFAULTS


def cmd_run(path, win):
    """Handle 'run <path>' command."""
    section(" Run ")
    ok_val, msg = validate_input_path(path)
    if not ok_val:
        fail(msg)
        section_end()
        return
    ok(f"Input: {path} ({msg})")
    dev_setting = load_settings().get("device", "auto")
    device = dev_setting if dev_setting in ("cpu", "cuda") else suggest_device()
    info(f"Device: {device} (setting: {dev_setting})")
    if msg == "video":
        success = process_video(path, device=device)
    else:
        success = process_image(path, device=device)
    if success:
        ok("Pipeline completed (stub).")
    else:
        fail("Pipeline failed.")
    section_end()


def cmd_validate(path, win):
    """Handle 'validate <path>' command."""
    section(" Validate ")
    ok_val, msg = validate_input_path(path)
    if ok_val:
        ok(f"Valid: {path} ({msg})")
    else:
        fail(msg)
    section_end()


def cmd_gpu(win):
    """Handle 'gpu' command."""
    section(" GPU ")
    gpus = get_gpu_info()
    if not gpus:
        warn("No NVIDIA GPU or nvidia-smi not available.")
        info("Device: CPU")
    else:
        for i, g in enumerate(gpus):
            line(g.get("raw", "GPU " + str(i)))
    section_end()


def cmd_about(win):
    """Show About from README: app name, version, description."""
    section(" About ")
    readme_path = os.path.join(_ROOT, "README.md")
    if os.path.isfile(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                lines = f.read().strip().split("\n")
            for ln in lines:
                ln = ln.strip()
                if ln.startswith("##") and "Settings" in ln:
                    break
                if not ln or ln == "---":
                    continue
                if ln.startswith("# "):
                    line(ln[2:].strip())
                elif "**Version**" in ln or "Version:" in ln:
                    line(ln.replace("**", "").strip())
                elif "Application" in ln or "Interface" in ln or "Requirements" in ln or "Python" in ln:
                    line(ln[: W - 4] if len(ln) > W - 4 else ln)
                elif ln.startswith("- `main.py`"):
                    line(ln[: W - 4] if len(ln) > W - 4 else ln)
        except Exception:
            pass
    if not os.path.isfile(readme_path):
        line("Security Research Toolkit")
        line("Version: 1.0.0")
        line("CMD Console Interface.")
    line("")
    line("README: " + readme_path)
    section_end()


def cmd_settings(win):
    """Show and edit settings (README: device, output_dir, log_level, language)."""
    section(" Settings ")
    s = load_settings()
    line("  device      = " + str(s.get("device", "auto")))
    line("  output_dir  = " + str(s.get("output_dir", "./output")))
    line("  log_level   = " + str(s.get("log_level", "info")))
    line("  language    = " + str(s.get("language", "ru")))
    line("")
    info("Change: enter key=value (e.g. device=cpu) or press Enter to skip.")
    section_end()
    try:
        raw = input("  > ").strip()
    except (EOFError, KeyboardInterrupt):
        return
    if not raw:
        return
    if "=" in raw:
        k, _, v = raw.partition("=")
        k, v = k.strip().lower(), v.strip()
        if k in DEFAULTS:
            if k == "log_level" and v not in ("debug", "info", "warning", "error"):
                warn("log_level: debug | info | warning | error")
                return
            if k == "device" and v not in ("auto", "cpu", "cuda"):
                warn("device: auto | cpu | cuda")
                return
            if k == "language" and v not in ("ru", "en"):
                warn("language: ru | en")
                return
            s[k] = v
            if save_settings(s):
                ok("Saved: " + k + " = " + v)
            else:
                fail("Could not save settings.")
        else:
            warn("Unknown key. Allowed: device, output_dir, log_level, language.")


def main_cli(args):
    """Non-interactive CLI."""
    banner()
    if args.validate:
        section(" Validate ")
        ok_val, msg = validate_input_path(args.validate)
        if ok_val:
            ok(f"Valid: {args.validate} ({msg})")
        else:
            fail(msg)
        section_end()
        return 0 if ok_val else 1
    if args.gpu:
        cmd_gpu(None)
        return 0
    if args.run:
        cmd_run(args.run, None)
        return 0
    # No action: show help
    section(" Usage ")
    line("  python main.py --run <video_or_image>")
    line("  python main.py --validate <path>")
    line("  python main.py --gpu")
    line("  python main.py --interactive")
    line("")
    section_end()
    return 0


def run_install_deps():
    """Install dependencies and show result."""
    section(" Install dependencies ")
    info("Running: pip install -r requirements.txt")
    if install_dependencies():
        ok("Dependencies installed successfully.")
        try:
            import gui.main_window
            importlib.reload(gui.main_window)
        except Exception:
            pass
    else:
        fail("Installation failed. Run manually: pip install -r requirements.txt")
    section_end()


def main_interactive():
    """Interactive CMD loop with launcher: [1] Install deps, [2] Start."""
    win = MainWindow()
    win.show_banner()

    while True:
        launcher_screen()
        try:
            choice = input("  Choose [1]-[4]: ").strip() or "2"
        except (EOFError, KeyboardInterrupt):
            break
        if choice == "1":
            run_install_deps()
            continue
        if choice == "2":
            deps_ok, missing = check_dependencies()
            if not deps_ok:
                warn("Missing dependencies: " + ", ".join(missing))
                try:
                    ans = input("  Install now? (Y/n): ").strip().lower() or "y"
                except (EOFError, KeyboardInterrupt):
                    break
                if ans in ("y", "yes"):
                    run_install_deps()
                else:
                    info("Starting without some dependencies (console styling may be limited).")
            break
        if choice == "3":
            cmd_about(win)
            continue
        if choice == "4":
            cmd_settings(win)
            continue
        warn("Enter 1, 2, 3 or 4.")

    win.show_menu()
    info("Enter command (run <path>, validate <path>, gpu, help, quit).")
    while True:
        try:
            raw = input("\n> ").strip()
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
            win.show_menu()
            continue
        if cmd == "run":
            cmd_run(arg, win)
            continue
        if cmd == "validate":
            cmd_validate(arg, win)
            continue
        if cmd == "gpu":
            cmd_gpu(win)
            continue
        if cmd in ("install", "1"):
            run_install_deps()
            continue
        if cmd == "about":
            cmd_about(win)
            continue
        if cmd == "settings":
            cmd_settings(win)
            continue
        warn(f"Unknown command: {cmd}. Type 'help' or 'quit'.")


@ensure_env
def main():
    parser = argparse.ArgumentParser(description="Neural Inpainting & SORA Detection (CMD)")
    parser.add_argument("--run", metavar="PATH", help="Process video or image")
    parser.add_argument("--validate", metavar="PATH", help="Validate input file")
    parser.add_argument("--gpu", action="store_true", help="Show GPU status")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive menu")
    args = parser.parse_args()
    if args.interactive or (not args.run and not args.validate and not args.gpu):
        if not args.run and not args.validate and not args.gpu:
            main_interactive()
            return 0
        if args.interactive:
            main_interactive()
            return 0
    return main_cli(args)


if __name__ == "__main__":
    sys.exit(main())
