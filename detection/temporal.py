# -*- coding: utf-8 -*-
"""Frame temporal analysis (consistency, flicker, interpolation)."""


def temporal_consistency(frames, window=5):
    """
    Compute temporal consistency score over a window of frames.
    Returns per-frame or global score.
    """
    if not frames:
        return []
    return [0.0] * len(frames)


def detect_interpolation(frames):
    """Detect likely interpolated frames. Returns list of frame indices."""
    return []
