# -*- coding: utf-8 -*-
"""File operations for video and image paths."""
import os
from .logger import warning, error


def ensure_dir(path):
    """Create directory if it does not exist."""
    if not path:
        return False
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except OSError as e:
        error(f"Cannot create directory {path}: {e}")
        return False


def is_video_file(path):
    """Check if path has common video extension."""
    if not path or not os.path.isfile(path):
        return False
    ext = os.path.splitext(path)[1].lower()
    return ext in (".mp4", ".avi", ".mkv", ".mov", ".webm", ".wmv", ".flv")


def is_image_file(path):
    """Check if path has common image extension."""
    if not path or not os.path.isfile(path):
        return False
    ext = os.path.splitext(path)[1].lower()
    return ext in (".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff", ".tif")


def safe_path(base_dir, name):
    """Return a path under base_dir with sanitized name."""
    safe_name = "".join(c for c in name if c.isalnum() or c in "._- ")
    return os.path.join(base_dir, safe_name.strip() or "output")
