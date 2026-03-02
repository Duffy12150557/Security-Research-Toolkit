# -*- coding: utf-8 -*-
"""Input validation for paths and options."""
import os
from utils.file_handler import is_video_file, is_image_file


def validate_input_path(path):
    """
    Validate input path: exists and is video or image.
    Returns (ok: bool, message: str).
    """
    if not path or not path.strip():
        return False, "Path is empty"
    path = path.strip()
    if not os.path.exists(path):
        return False, f"Path does not exist: {path}"
    if not os.path.isfile(path):
        return False, f"Not a file: {path}"
    if is_video_file(path):
        return True, "video"
    if is_image_file(path):
        return True, "image"
    return False, f"Unsupported format. Use video or image: {path}"


def validate_output_dir(path):
    """Check output directory can be used (exists or can be created)."""
    if not path:
        return False, "Output path is empty"
    if os.path.isfile(path):
        return False, "Output path is a file, not a directory"
    return True, "ok"
