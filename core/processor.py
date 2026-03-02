# -*- coding: utf-8 -*-
"""Video processing pipeline: load -> detect -> inpaint -> save."""
from .validator import validate_input_path
from .inpainting import inpaint_frame
from utils.logger import info, warning, error


def process_video(input_path, output_dir=None, device="cpu"):
    """
    Full pipeline: validate -> load frames -> run detection -> inpaint -> write.
    Returns success: bool.
    """
    ok_val, msg = validate_input_path(input_path)
    if not ok_val:
        error(msg)
        return False
    info(f"Input type: {msg}")
    # Stub: no actual frame loading; real impl would use opencv/ffmpeg
    info("Pipeline: load frames -> detect -> inpaint -> save (stub)")
    return True


def process_image(input_path, output_path=None, device="cpu"):
    """Process single image through detection + inpainting."""
    ok_val, msg = validate_input_path(input_path)
    if not ok_val:
        error(msg)
        return False
    info("Image pipeline (stub): validate -> detect -> inpaint -> save")
    return True
