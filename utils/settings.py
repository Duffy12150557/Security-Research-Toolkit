# -*- coding: utf-8 -*-
"""Application settings (see README.md). Load/save settings.json."""
import json
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SETTINGS_PATH = os.path.join(_ROOT, "settings.json")

DEFAULTS = {
    "device": "auto",
    "output_dir": "./output",
    "log_level": "info",
    "language": "en",
}


def _path():
    return _SETTINGS_PATH


def load():
    """Load settings from settings.json. Return dict (defaults + file)."""
    out = DEFAULTS.copy()
    if not os.path.isfile(_SETTINGS_PATH):
        return out
    try:
        with open(_SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k in DEFAULTS:
            if k in data:
                out[k] = data[k]
    except Exception:
        pass
    return out


def save(settings):
    """Save settings dict to settings.json. Only known keys."""
    data = {k: settings.get(k, DEFAULTS[k]) for k in DEFAULTS}
    try:
        with open(_SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def get(key, default=None):
    return load().get(key, default or DEFAULTS.get(key))


def set_key(key, value):
    if key not in DEFAULTS:
        return False
    s = load()
    s[key] = value
    return save(s)
