# -*- coding: utf-8 -*-
"""CNN detection engine for region/artifact detection (stub)."""


def detect_regions(frame, model_name="stub"):
    """
    Run CNN on a frame to get regions of interest (e.g. artifacts, tampering).
    Returns list of dicts: [{"bbox": (x,y,w,h), "score": float, "label": str}, ...]
    """
    # Stub: no model loaded
    return []


def load_model(device="cpu", model_path=None):
    """Load detection model. Returns model object or None."""
    return None
